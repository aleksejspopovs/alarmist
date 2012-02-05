import ctypes
from BaseSensor import BaseSensor
from AlarmistExceptions import WrongOptionsError, NotSupportedError

class SensorData(ctypes.Structure):
	_fields_ = [
		('status', ctypes.c_int),
		('raw_x', ctypes.c_short),
		('raw_y', ctypes.c_short),
		('x', ctypes.c_short),
		('y', ctypes.c_short),
		('temp', ctypes.c_byte),
		('center_x', ctypes.c_short),
		('center_y', ctypes.c_short),
	]

class ThinkPadShockSensor(BaseSensor):
	"""
	An Alarmist sensor that uses Sensor.dll to get data from your ThinkPad's aceelerometer (APS).
	Will throw NotSupportedError if you don't have a ThinkPad or Sensor.dll isn't installed.
	Options[0] is the panic threshold (when your TP's unstability reaches it, the sensor panics). On my x121e, unstability is between 0 and 9
	  and I find 4 to be the ideal threshold. Options[1] is the delay between checks.
	Only works on Windows and under 32-bit versions of Python.
	"""
	def __init__(self, options, panicCallback, stopPanicCallback):
		BaseSensor.__init__(self, options, panicCallback, stopPanicCallback)

		try:
			self.panicThreshold = options[0]
			self.delay = options[1]
		except:
			raise WrongOptionsError('ThinkPadShockSensor')

		try:
			self.func = ctypes.windll.Sensor.ShockproofGetAccelerometerData
		except:
			raise NotSupportedError('ThinkPadShockSensor')

	def checkIfWeAreScrewed(self):
		data = SensorData()
		self.func(ctypes.byref(data))
		return data.status >= self.panicThreshold
