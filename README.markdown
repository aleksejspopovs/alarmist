About Alarmist
==============

Alarmist is a piece of software for paranoids just like me. In short, Alarmist periodically asks *sensors* if something wrong is going on and, if the sensors respond positively, initiates a *panic*.

An example usage is the default ThinkPad Shock Sensor and the default hibernation panic. When combined, those will make your ThinkPad hibernate whenever it's moving for a long enough time (i.e. if someone's lifted it up and is trying to steal it). If you use system encryption, then this is a wonderful way to solve one of the most serious problems of system encryption: the danger of your laptop being stolen while it's turned on. There's a [video on YouTube](http://www.youtube.com/watch?v=l0SKIhsyJqQ) demonstrating this example.

Details on inner workings
=========================

Alarmist itself relies on three modules to work:

- the *sensor* is responsible for notifying Alarmist whenever something weird is going on
	- **ThinkPadShockSensor** is the only included sensor at the moment. It checks if your laptop is moving. Unfortunately, it only works on [ThinkPad laptops with accelerometers](http://www.thinkwiki.org/wiki/Active_Protection_System) and only supports 32-bit Python on Windows (although it is possible to port it to Linux)
- the *panic manager* is responsible for quickly doing whatever you might want it to do whenever Alarmist tells it someting's wrong
	- the only included panick manager is **CMDPanic**, which runs a specified application during panic events. CMDPanic supports any OS.
- the *user interface* is responsible for notifying you about what's going on and allowing you to temporarily turn Alarmist off
	- one of the included UIs is **WXTaskbarUI**, which creates a nice icon in your taskbar and allows you to toggle Alarmist state by either double-clicking the icon or using the system-wide hotkey (which is Alt-F1 by default, but you're free to change it). As the name implies, WXTaskbarUI uses wxPython and therefore requires wxPython to be installed. Even though I didn't try to use WXTaskbarUI under any OS other than Windows, I believe it will work under any OS.
	- the other is **ConsoleUI**. ConsoleUI is mainly for development purposes, although you're free to try it if you can't/don't want to use WXTaskbarUI for some reason.

More info on each module is available in it's corresponding .py file (e.g. ThinkPadShockSensor.py)

Configuration and usage
=======================

Configuration is done via a file named `config.py`. It should be pretty straightforward to modify and there are comments near most of the fields, so I'll assume there's no need to discuss configuration.

Launching Alarmist is as easy as simply typing

	cd ./alarmist
	python ./alarmist.py

in your command prompt. However, Windows users (and maybe some other OS users too) might want to use `pythonw` instead of `python`, because otherwise they'll get a practically useless command prompt window (unless you use ConsoleUI, of course).

Everything else, obviously, depends on the UI you are using. WXTaskbarUI should pretty much straightforward:

![WXTaskbarUI screenshot](http://s1.hostingkartinok.com/uploads/images/2012/02/34d517876f0a56f91525a97d0ab64484.png)

The big rectangle on the left displays the current state of Alarmist (red means unarmed, green means armed). The smaller rectangle on the right is a 'panic meter' that fills with red when the sensor is reporting danger (the speed at which it fills up is defined by the timeout variable in `config.py`). Double-clicking the icon or using the hotkey you defined in `config.py` will toggle the state of Alarmist, right-clicking the icon will open the menu that allows you to either toggle the state of Alarmist (again!) or exit Alarmist.

Contributing to Alarmist
========================

If you wish to help me add features to Alarmist (for example, I'd love to see some new interesting sensors) or make the existing features better (e.g. port ThinkPadShockSensor to Linux), you may send me pull requests. If you have any questions regarding how something works or what's the best way to implement your idea, [contact me](http://popoffka.ru) and I'll be glad to help you.

By the way, Alarmist is licensed under MIT License, see LICENSE for more info.

Donations
=========

If you really really like Alarmist, feel free to donate. Or not to donate.

[![PayPal - The safer, easier way to pay online!](https://www.paypalobjects.com/en_US/i/btn/btn_donate_LG.gif)](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=TZWCNZQ6N9KYJ)
