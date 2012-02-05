from BaseUI import BaseUI
from threading import Thread

class ConsoleUI(BaseUI):
	'''
	A very simple console-based UI for the Alarmist.
	Not really intended for actual use, more of a development tool (although it seems to be functional
	  and you're free to try to use it).
	Doesn't have any options.
	Seems to work under any OS.
	'''
	def monitorInput(self):
		while (True):
			command = raw_input()
			if command.strip() == 'toggle':
				self.toggleCallback()
			elif command.strip() == 'exit':
				self.exitCallback()

	def __init__(self, options, toggleCalback, exitCallback, initState):
		BaseUI.__init__(self, options, toggleCalback, exitCallback, initState)
		print 'ConsoleUI: state is ', self.state
		t = Thread(group=None, target=self.monitorInput, name=None)
		t.start()

	def changeState(self, state):
		print 'ConsoleUI: state changed to',state

	def changePanicState(self, state):
		print 'ConsoleUI: panic at',state
