from threading import Thread, Event
class PeriodicTimer(Thread):
	"""Call a function every /interval/ seconds:

	t = PeriodicTimer(30.0, f, args=[], kwargs={})
	t.start()
	t.cancel()
	"""

	def __init__(self, interval, function, limit=None, finishCallback=None, args=[], kwargs={}):
		Thread.__init__(self)
		self.interval = interval
		self.function = function
		self.limit = limit
		self.finishCallback = finishCallback
		self.args = args
		self.kwargs = kwargs
		self.finished = Event()

	def cancel(self):
		"""Stop the timer if it hasn't finished yet"""
		self.finished.set()

	def run(self):
		i = 0
		while (not self.finished.is_set()) and (not self.limit or i < self.limit):
			self.finished.wait(self.interval)
			if not self.finished.is_set():
				self.function(*self.args, **self.kwargs)
			i += 1

		if not self.finished.is_set() and self.limit and self.finishCallback:
			self.finishCallback()
