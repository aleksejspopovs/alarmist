class BaseUI():
	def __init__(self, options, toggleCallback, exitCallback, initState):
		# you should save the toggleCallback and initState, I guess
		self.toggleCallback = toggleCallback
		self.exitCallback = exitCallback
		self.state = initState

	def changeState(self, state):
		# 0 means unarmed
		# 1 means armed
		pass

	def changePanicState(self, state):
		# 0 < x < 1 means panicking and part x of the timeout has passed
		pass

	def close(self):
		# if you have to destroy anything, feel free to do it right now
		pass
