from PeriodicTimer import PeriodicTimer

class BaseSensor():
	def __init__(self, options, panicCallback, stopPanicCallback):
		# you should probably save the callbacks and do something with the options
		# if options are wrong, raise WrongOptionsError
		# if the sensor is not suported (i.e. a required dll isn't installed), raise NotSupportedError
		self.delay = 1
		self.timer = None
		self.panicking = False
		self.panicCallback = panicCallback
		self.stopPanicCallback = stopPanicCallback

	def checkIfWeAreScrewed(self):
		# this function is NOT required and will not be called by the program itself
		# however, functions start() and stop() below use it, so if you're too lazy to write your own start() and stop(),
		# you can simply redefine this function
		return False

	def handleData(self):
		# same as above, basically
		res = self.checkIfWeAreScrewed()
		if res and (not self.panicking):
			self.panicking = True
			self.panicCallback()
		elif (not res) and self.panicking:
			self.panicking = False
			self.stopPanicCallback()

	def start(self):
		# start periodic checks
		if self.timer:
			return

		self.timer = PeriodicTimer(self.delay, self.handleData)
		self.timer.start()

	def stop(self):
		# stop periodic checks
		if not self.timer:
			return

		self.timer.cancel()
		self.timer = None

	def close(self):
		# close all the handles and shit
		pass
