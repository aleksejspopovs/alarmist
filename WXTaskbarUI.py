import wx
import string
from BaseUI import BaseUI
from threading import Thread
from AlarmistExceptions import WrongOptionsError

ID_TOGGLE_MENUEL = wx.NewId()
ID_HOTKEY = wx.NewId()

class IconBar:
	def __init__(self,l_off=[255,0,0],l_on=[0,255,0],r_off=[0,128,0],r_on=[0,255,0]):
		self.s_line = '\xff\xff\xff' + '\0\0\0' * 14 + '\xff\xff\xff'
		self.s_point = '\0' * 3
		self.sl_off = string.join(map(chr, l_off), '') * 10
		self.sl_on = string.join(map(chr, l_on), '') * 10
		self.sr_off = string.join(map(chr, r_off), '') * 3
		self.sr_on = string.join(map(chr, r_on), '') * 3

	def Get(self, l, r):
		s = '' + self.s_line
		for i in range(14):
			sl = l and self.sl_on or self.sl_off
			sr = (14 - i) / 14.0 > r and self.sr_off or self.sr_on
			s += self.s_point + sl + self.s_point + sr + self.s_point
		s += self.s_line

		image = wx.EmptyImage(16, 16)
		image.SetData(s)

		bmp = image.ConvertToBitmap()
		bmp.SetMask(wx.Mask(bmp, wx.WHITE))

		icon = wx.EmptyIcon()
		icon.CopyFromBitmap(bmp)

		return icon

class MyTaskBarIcon(wx.TaskBarIcon):
	def __init__(self, frame):
		self.armStatus = True
		self.panicStatus = 0

		wx.TaskBarIcon.__init__(self)
		self.frame = frame
		self.IconBar = IconBar((255,0,0), (0,255,0), (255,192,203), (255,0,0))
		self.SetIconBar()

	def SetIconBar(self):
		icon = self.IconBar.Get(self.armStatus, self.panicStatus)
		status = 'Alarmist: '
		if not self.armStatus:
			status += 'un'
		status += 'armed; '
		if not self.panicStatus:
			status += 'no '
		else:
			status += '%.2f ' % (self.panicStatus)
		status += 'panic'
		self.SetIcon(icon, status)

	def CreatePopupMenu(self):
		menu = wx.Menu('')
		menu.Append(ID_TOGGLE_MENUEL, 'Toggle state', '')
		menu.Append(wx.ID_EXIT, 'Exit', '')
		return menu

class TaskBarApp(wx.Frame):
	def __init__(self, parent, id, title, options):
		wx.Frame.__init__(self, parent, -1, title, size = (1, 1),
			style=wx.FRAME_NO_TASKBAR | wx.NO_FULL_REPAINT_ON_RESIZE)

		self.tbicon = MyTaskBarIcon(self)
		if (options[0]):
			if not self.RegisterHotKey(ID_HOTKEY, options[1], options[2]):
				raise WrongOptionsError('WXTaskbarUI')
		self.Show(True)

class WXTaskbarUIApp(wx.App):
	def __init__(self, *args, **kwargs):
		self.toggleCallback = kwargs['toggleCallback']
		self.exitCallback = kwargs['exitCallback']
		self.options = kwargs['options']
		del kwargs['toggleCallback']
		del kwargs['exitCallback']
		del kwargs['options']
		wx.App.__init__(self, *args, **kwargs)

	def onMenu(self, event):
		if (event.Id == wx.ID_EXIT):
			self.exitCallback()
		elif (event.Id == wx.ID_TOGGLE_MENUEL):
			# toggle
			self.toggleCallback()

	def onToggleEvent(self, event):
		# toggle
		self.toggleCallback()


	def OnInit(self):
		self.frame = TaskBarApp(None, -1, '', self.options)
		self.frame.Center(wx.BOTH)
		self.frame.Show(False)

		self.Bind(wx.EVT_MENU, self.onMenu)
		self.Bind(wx.EVT_TASKBAR_LEFT_DCLICK, self.onToggleEvent)
		self.Bind(wx.EVT_HOTKEY, self.onToggleEvent, id=ID_HOTKEY)
		return True

class WXTaskbarUI(BaseUI):
	"""
	A wxPython-based UI that creates an icon in the taskbar taht displays the state of security.
	WXTaskbarUI is also able to create system-wide hotkeys.
	Options should be an iterable object. If options[0] is False, then all other contents of options
	  are ignored. Otherwise, options[1] is treated as modifier and options[2] as the keycode of the hotkey.
	This should theoretically work under any OS, although the modifier and key codes might differ.
	"""
	def __init__(self, options, toggleCallback, exitCallback, initState):
		try:
			options[0] and options[1] and options[2]
		except:
			raise WrongOptionsError('WXTaskbarUI')
		self.options = options
		self.toggleCallback = toggleCallback
		self.exitCallback = exitCallback
		self.initState = initState
		self.thread = Thread(group=None, target=self.launchApp)
		self.thread.start()

	def launchApp(self):
		self.app = WXTaskbarUIApp(0, toggleCallback=self.toggleCallback, exitCallback=self.exitCallback, options=self.options)
		self.changeState(self.initState)
		self.app.MainLoop()

	def changeState(self, state):
		self.app.frame.tbicon.armStatus = state
		self.app.frame.tbicon.SetIconBar()

	def changePanicState(self, state):
		self.app.frame.tbicon.panicStatus = state
		self.app.frame.tbicon.SetIconBar()

	def close(self):
		self.app.Destroy()
