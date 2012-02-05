from ThinkPadShockSensor import ThinkPadShockSensor
from CMDPanic import CMDPanic
from ConsoleUI import ConsoleUI
# from WXTaskbarUI import WXTaskbarUI # windows-only!

# anymoduleOptions is a variable that gets passed to the module, so the expected contents might (and will)
#   differ between modules. to get more information on that, refer to the docstring for the respective
#   module (e.g. ThinkPadShockSensor.__doc__ or line 18-24 of ThinkPadShockSensor.py)

sensor = ThinkPadShockSensor
sensorOptions = [4, 1.0]

panic = CMDPanic
panicOptions = 'shutdown /h'

UI = ConsoleUI
UIOptions = [True, 1, 112]

# initState defines the initial state of security (True means armed, False means unarmed)
initState = True
# timeout defines time (in seconds) between the first panic signal from the sensor until actual panic is performed
# 0 means that the panic action will be performed as soon as there's any danger data from the sensor
timeout = 5
