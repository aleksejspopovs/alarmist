class WrongOptionsError(Exception):
	def __init__(self, module):
		self.module = module

class NotSupportedError(Exception):
	def __init__(self, module):
		self.module = module
