from AlarmistExceptions import *
from PeriodicTimer import PeriodicTimer
import os

class Alarmist():
	def __init__(self, panic, panicOptions, sensor, sensorOptions, UI, UIOptions, initState, timeout):
		self.state = initState
		self.panicM = panic(panicOptions)
		self.sensor = sensor(sensorOptions, self.panic, self.stopPanic)
		self.UI = UI(UIOptions, self.toggle, self.exit, self.state)
		self.panicTimer = None
		self.timeout = timeout
		self.timePassed = 0

		if (self.state):
			self.sensor.start()

	def exit(self):
		self.sensor.stop()
		self.sensor.close()
		self.UI.close()
		os._exit(0)

	def realPanic(self):
		self.panicM.panic()
		self.exit()

	def updateState(self):
		self.timePassed += 1
		self.UI.changePanicState(float(self.timePassed) / self.timeout)

	def panic(self):
		if not self.timeout:
			self.realPanic()
		else:
			self.timePassed = 0
			self.panicTimer = PeriodicTimer(1.0, self.updateState, self.timeout, self.realPanic)
			self.panicTimer.start()

	def stopPanic(self):
		if not self.panicTimer:
			return

		self.panicTimer.cancel()
		self.panicTimer = None
		self.state = True
		self.UI.changePanicState(0)
		self.UI.changeState(self.state)

	def toggle(self):
		self.state = not self.state
		if (self.state):
			self.sensor.start()
		else:
			self.sensor.stop()
			if (self.panicTimer):
				self.panicTimer.cancel()
				self.panicTimer = None
		self.UI.changeState(self.state)

if __name__ == '__main__':
	import config
	alarmist = Alarmist(config.panic, config.panicOptions,
		config.sensor, config.sensorOptions,
		config.UI, config.UIOptions,
		config.initState, config.timeout)
