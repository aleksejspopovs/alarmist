from BasePanic import BasePanic
from threading import Thread
from subprocess import Popen

class CMDPanic(BasePanic):
	"""
	Launches the specified application using subprocess.Popen.
	Options should either be a string or an iterable object with strings
	  (i.e., 'shutdown /h' or ['shutdown', '/h'])
	Should work under any OS.
	"""
	def __init__(self, options):
		self.command = options

	def panic(self):
		Popen(self.command)
