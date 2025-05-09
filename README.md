# ittyWxV3
ittyWxV3 (Internet Weather for Teletype version 3)

(version 3 supersedes version 1)


This readme will help you get going with ittyWx - Internet Weather for Teletype!  ittyWxV3 will allow you to get near real time weather alerts & bulletins, current conditions and forecasts from the National Weather Service API servers -- printed out straight onto your Teletype!

These python scripts have been written to run on a Raspberry Pi, connected via a Volpe USB-Teletype (v2) board, with or without a 5v power relay.  These scripts may also run on other CPUs using Python, but ideally with use on a Raspberry Pi 5.  Please keep all files in one folder, in order for these scripts to work properly.

What you need to do, in order to use ittyWx:


1 -- Get a National Weather Service API key.  Not having a key may and will cause IP blocks -- and signing up is free!  You can register for your own key here:

	https://api.data.gov/signup/

...and please do not share your key with anyone - it is yours only.  With this key, you can make up to 1,000 data requests per hour with the Weather Service (as of 2020) without restrictions nor daily limits.  Once you have your key, please enter it in section 1 (API key) of the settings.py script file -- between the quotation marks.  The code format is as follows (key):

	APIKey = ""	(your API key goes between the quotation marks)


2 -- In ittyWxV3, you can receive weather bulletins from the areas of your choice.  These areas can be zones, counties and/or states (and multiple locations if desired).  The code format is as follows (alpha/numeric or alpha):

	["ABC123", "zone"], 	(for zones/counties)
	["XX", "area"],		(for states)

 * For zones or counties, the code for those areas are three alphas and three numerics.  To find these codes, please go to the URL below:...

	https://alerts.weather.gov/

...click on "Land areas with zones", then to the right of any state listed, click on either the "Public Zones" or "County Zones" links (Disregarding the "ATOM" links) -- these two links will lead you to the zone/county codes that you'll want/need.  Finally, copy/paste the zone/county code(s) into section 2 (alerts) of the settings.py script file.

 * For statewide alerts, it's as simple as entering the two-letter state abbreviation for that state.

One very important note to make is that in Python, adding a number sign ( # ) will "comment out" whatever comes after it on that same line... so in other words, using a number sign will make everything to the right of it, on that same line, invisible to Python.  Use # to enable or delete # to disable lines, as needed.


3 -- ittyWxV3 will check the NWS API servers for alerts for given zones at specified intervals.  The number in Section 3 (scrape frequency) of the settings.py script file will be this interval in seconds.  The minimum is 3.7 seconds... please DO NOT go below 3.7 seconds or else IP blocks may happen.  The code format is as follows (numeric -- as an example):

	sleeptime = 3.7		(the script will scrape for alerts every 3.7 seconds)


4 -- ittyWxV3 can also check for current conditions and forecasts!  Section 4 (current conditions and forecasts locations) of the settings.py script file specifies these locations.  The code format is as follows (alpha/numeric -- as an example):

	["ABCD", [12.3456789, -12.3456789]],	(station code/coordinates)

 * Station codes are for current conditions and are four-letter codes.  You can look up the nearest weather station that you want current conditions for by going here:

	https://tinyurl.com/nwsstations

 * Coordinates are for weather forecasts issued by the nearest NWS Weather Forecast Office nearest to those coordinates.  These Latitude/Longitude coordinates are in Decimal Degrees format and may be acquired by various means (i.e. on Google Maps or by GPS).  Coordinates may be rounded to the nearest ten-millionth of a degree.

 ** Alternatively, if you wish to receive current conditions only and not forecasts, the code format is as follows (alpha):

	["ABCD", []],	(station code/null)

 ** ...and the other way around -- if you wish to receive forecast only and not current conditions, the code format is as follows (numeric -- as an example):

	["", [12.3456789, -12.3456789]],	(null/coordinates)

Like alerts, you may pull current conditions and forecasts from as many areas as you'd like, by entering additional lines in section 4 of the settings.py script file - as formatted above.


5 -- You can choose when to print current conditions onto your Teletype.  You can specify when by inputing the hour, in military time, into section 5 (hours to print current conditions) of the settings.py script file.  The script will print current conditions for locations as specified in section 4 of the settings.py script file, at the top of the hour, as specified.  The code format is as follows (numeric and with commas, as needed -- as examples):

	"Monday": [],				(will NOT print during any hours on Monday)
	"Tuesday": [0, 1, 2, 3, 4, 5, 6],	(will print all hours from midnight through 6am on Tuesdays)
	"Wednesday": [7, 8, 9, 10, 11, 12],	(will print all hours from 7am through noon on Wednesdays)
	"Thursday": [13, 14, 15, 16, 17, 18],	(will print all hours from 1pm through 6pm on Thursdays)
	"Friday": [19, 20, 21, 22, 23],		(will print all hours from 7pm through 11pm on Fridays)
	"Saturday": [12],			(will print only at noon on Saturdays)
	"Sunday": [5, 9, 14, 20],		(will print only at 5am, 9am, 2pm and 8pm on Sundays)


6 -- You can choose when to print forecasts onto your Teletype.  You can specify when by inputing the hour, in military time, into section 6 (hours to print forecasts) of the settings.py script file.  The script will print forecasts for locations as specified in section 4 of the settings.py script file, at the top of the hour, as specified.  The code format is as follows (numeric and with commas, as needed -- as examples):

	"Monday": [16],				(will print only at 4pm on Mondays)
	"Tuesday": [2, 3, 4, 5, 16],		(will print all hours from 2am through 5am and also 4pm on Tuesdays)
	"Wednesday": [9, 10, 11],		(will print all hours from 9am through 11am on Wednesdays)
	"Thursday": [13, 14, 15, 16],		(will print all hours from 1pm through 4pm on Thursdays)
	"Friday": [19, 20, 21, 22, 23],		(will print all hours from 7pm through 11pm on Fridays)
	"Saturday": [],				(will NOT print during any hours on Saturday)
	"Sunday": [4, 11, 18, 21, 22],		(will print only at 4am, 11am, 6pm, 9pm and 10pm on Sundays)


7 -- You can choose how many forecast periods are printed for each forecast -- this will be a global setting for all forecasts.  For example, entering the number 1 in section 7 (forecast periods) of the settings.py script file will only print the forecast for "This Afternoon", if on a Monday afternoon.  Entering the number 3 will print 3 periods... again, if on a Monday afternoon and just as an example -- would print "This Afternoon", "Tonight" and "Tuesday".  The maximum periods that will print are generally 14 (depending on the time of day when the forecasts are printed) and of course, will also be dependent on the settings in both section 6 and section 4 of the settings.py script file.  The code format is as follows (numeric -- as an example):

	number_of_forecast_periods = 5		(forecasts will print only five periods)


8 -- You can tell ittyWxV3 script when to do nothing... i.e. don't scrape for alerts nor print alerts, current conditions or forecasts (in other words, go to sleep!).  This is particularly useful for times when you want to sleep yourself and not have the Teletype nearby wake you up, etc.  The hours in section 8 (quiet hours) of the settings.py script file are in military time and the code format is as follows (numeric and with commas, as needed -- as a, example):

	quiet_hours = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11]		(nothing will scrape nor print between 2am and 11am).

Please note that any hours inputed in section 8 will override any hours specified in sections 5 and 6 of the settings.py script file.


9 -- Section 9 (console print / military time) of the settings.py script file are miscellaneous settings.  If running on a Raspberry Pi (or equivalent), the log_alerts setting will allow alert activity to be printed to the console (True) or not printed (False).  The military_time setting will display times either in military time (False) or am/pm (True).  The code format is as exampled below (True/False):

	log_alerts = True		(print alerts to console)
	military_time = False		(print in military time)


10 -- Section 10 (VolpeV2 serial address) of the settings.py script file is a miscellaneous settings.  Typically the VolpeV2 board serial address will most always be "/dev/ttyACM0" (if with only one board) - and the code format is as follows (address):

	SERIALPORT = "/dev/ttyACM0"	(serial address)

If in doubt, open Terminal and type:

	dmesg | grep tty

The Volpe board should read out as "ttyACM0: USB ACM device" or "ttyACM1: USB ACM device", etc.  The first part -- usually ttyACM0, is the address (copy/paste at the end of the address, as shown above, if needed).


11 -- Section 11 (power relays) of the settings.py script file is a miscellaneous settings and knowledge of the GPIO pinout on a Raspberry Pi board is 100% necessary for the second setting (Google is your friend!).  ittyWxV3 is built to work with a 5v power relay board.  The using_relay setting is either 0 (not using a relay) or 1 (using a relay).  The relay_GPIO_pin setting is the GPIO relay pin number - and the code format is as follows (numeric -- as an example):

	using_relay = 0		(not using a relay)
	relay_GPIO_pin = 17	(GPIO relay pin number)

 * For the relay_GPIO_pin setting -- if you are not using a power relay, you can just ignore this line (and leave as-is).


12 -- Section 12 (Mac debugging) of the settings.py script file is a miscellaneous settings and will almost always not be used/needed as a setting outside of debugging on a Mac computer.  The code should always be set to 0; otherwise, 1 if debugging on a Mac.  The code format should be as follows (numeric -- as an example):

	mac = 0		(not in a Mac debugging mode)


13 -- The following dependency should be entered into Terminal and installed onto a Raspberry Pi (and possibly equivalent systems running Python), in order for these scripts to work properly:

	sudo apt install python3-dateutil


14 -- Finally, open up the ittyWxV3.py script file and run it.  You should be good to go!


Fun facts / more info:

* ittyWxV3.py is the main script to run... all the other files are support or extra files.

* With a web scrape at every 3.7 seconds, you will stay below the 1,000/hour threshold with the NWS (as long as you have an API key registered).

* The script has a built-in garbage collector, which helps free up memory every 45 minutes.

* The script will now first check if all codes (alerts/stations/coordinates) are correct before checking/printing.  If there is an incorrect code, the script will automatically stop and help you pin down which code it may be.  It may take multiple runs when checked, if there are multiple code errors.

* The alert bell system:  10 bells for a Warning; 5 for a Watch; and 4 for an Advisory, statement or anything else.

* The format of the bulletins have been coded to look almost exactly how they would have originally appeared on the old Weather Wire back in the day.

* This script will only print any new alert received only once.

* This software is free to use.  If any bugs are found, please contact me.

* A special thank you to Faizan Mustafa for patiently working with me ittyWx (v1) and getting these scripts exactly right, without even having a Teletype to test them on!  Also a big thank you to Paul Heller for working on ittyWxV2 and getting these scripts cleaned up / very much improved!  I've personally lost count, but I believe at this point, four to five people have now contributed to the writing of ittyWxV3.


Possible issues:

* Raspberry Pis may cease to function or error out during extended runs of the ittyWxV3 script.  It is unknown if this is still an issue with Raspberry Pis 5 and will be investigated if found to be the case.

* There may be an API issue when the script checks for valid stations... it is unknown at this time whether this is the case or not.

* The fix to wind gusts properly being displayed has not been tested yet, at there seems to have been a change in the NWS API servers, which doesn't list them as frequently or at all.


Version history:

* ittyWx (v1) was released in 2020.  Version 1 only checked for / printed out weather bulletins and was originally tested to run on a Raspberry Pi 3 Model B+ (the current model at the time).

* ittyWxV2 was completed in 2021 and was not released publicly.  ittyWxV2:
 ** Added current conditions and forecasts.
 ** Fixed and reworked coding.
 ** Formatting fixes.
 ** Indentations added.
 ** Reworked how API requests are sent.
 ** Added the settings file and consolidated the API key into it, eliminating the need for the requests.auth file.
 ** Added sleep hours and times to print.
 ** Added other miscellaneous settings.
 ** Reformatted (clock) time printouts and added the option for military time. 
 ** Added garbage collecting.
 ** Added additional terminal printouts.
 ** Other miscellaneous fixes.


* ittyWxV3 was released in 2025 for the Raspberry 5 and:
 ** Fixed coding for the new NWS API calls.
 ** Added checks for stations and codes, which prevents hanging.
 ** The script will now automatically terminate if there is a code/coordinate or any other type of error and will turn off the 5v relay (if on) -- if such an error occurs (to prevent power supplies from overheating).
 ** If a wind speed unavailable at a weather station, then "mph" will no longer be a rogue print under current conditions.
 ** The percent symbol will now be printed as "percent", there will be a double space at the end of sentences and other grammar fixes.
 ** Additional formatting fixes/changes.
 ** Additional indentations added.
 ** NWS WFOs are now properly formatted for current conditions.
 ** Reformatted the settings file.
 ** Added additional terminal printouts.
 ** Other miscellaneous fixes.


ittyWxV3 (Internet Weather for Teletype version 3)
-tenko23
GNU GPLv3
