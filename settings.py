# SETTINGS FILE


# The following dependency should be entered into Terminal on a Raspberry Pi, in order for these scripts to work properly:
# Please omit the # symbol:...
#	sudo apt install python3-dateutil


# (1) API key:
#  Below is your NWS API key... you can get one here:  https://api.data.gov/signup/  .  Please paste the key between the quotation marks ("") and without spaces:

APIKey = ""		#Your NWS API key.  DO NOT share this key with anyone.


# (2) Alerts:
#  Public/county zone codes can be found at this link here:  https://alerts.weather.gov/ -> Land areas with zones (please disregard the ATOM links).

alert_locations = [			# DO NOT modify this line.  Add one or more lines below the following lines, for additional areas to monitor alerts.

    ["NEC109", "zone"],		# This line is an example of a county/zone to monitor for alerts.
    #["NE", "area"],		# This line is an example of a state to monitor for alerts (currently commented out).

    ]						# DO NOT modify this line, however it can be moved down when adding areas, by keeping the same tabbed format.


# (3) Scrape frequency:
#  The number below specifies (in seconds) the interval in which alerts are checked for a specified county(/ies)/zone(s)/state(s):

sleeptime = 3.7		#Increase this number to decrease the frequency of web-scrapes.  The minimum allowed via AIP is 3.7 seconds (please DO NOT go below or else IP blocks may happen).


# (4) Current conditions and forecasts locations:
#  You can look up your nearest weather station by going here:  https://tinyurl.com/nwsstations .

conditions_and_forecast_locations = [		# DO NOT modify this line.  Add one or more lines below the following lines, for additional areas to monitor for conditions/forecasts.

    ["KLNK", [40.8136350, -96.7070120]],	# This line is an example of getting both current conditions and forecasts.
    #["KLNK", []],							# This line is an example of getting current conditions only (currently commented out).
    #["", [40.8136350, -96.7070120]],		# This line is an example of getting forecasts only (currently commented out).
    
    ]										# DO NOT modify this line, however it can be moved down when adding areas, by keeping the same tabbed format (currently commented out).


# (5) Hours to print current conditions:
#  When to print current conditions (in military time) -- for all stations entered in the conditions_and_forecast_locations section:

days_hours_conditions = {		# DO NOT modify this line.

    "Monday": [8, 18],  		# Print at 8am and 6pm on Mondays.
    "Tuesday": [],  			# Will not print on this day.
    "Wednesday": [0],   		# Print at 12am on Wednesdays.
    "Thursday": [],
    "Friday": [21], 			# Print at 9pm on Wednesdays.
    "Saturday": [],
    "Sunday": [6, 10, 13, 19],	# Print at 6am, 10am, 1pm and 7pm on Sundays.

    }							# DO NOT modify this line


# (6) Hours to print forecasts:
#  When to print forecasts (in military time) -- for coordinates entered in the conditions_and_forecast_locations section:

days_hours_forecasts = {	# DO NOT modify this line.

    "Monday": [],   		# Will not print on this day.
    "Tuesday": [],
    "Wednesday": [],
    "Thursday": [12, 23],	# Print at 12pm and 11pm on Thursdays.
    "Friday": [2],			# Print at 2am on Fridays.
    "Saturday": [11, 14],	# Print at 11am and 2pm on Saturdays.
    "Sunday": [],

    }						# DO NOT modify this line.


# (7) Forecast periods:
#  The number below specifies how many forecasts periods (day/night, as applicable) to print for every NWS forecast (for all coordinates entered in the conditions_and_forecast_locations section... each forecast typically covers seven days).  The maximum number of periods is around 14:

number_of_forecast_periods = 5		# The number at the end of this line specifies how many forecast periods to print.


# (8) Quiet hours:
#  Which hours, in military time, not to run these scripts (check for alerts, print, etc.):

quiet_hours = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11]		# Nothing will web-scrape or print during these hours (as exampled here - from 2am through 11am).


# (9) Console print / military time:
#  The following two lines are not critical and may be left as-is:

log_alerts = True			#True:  Print alerts to console; False:  Do not print alerts to console"
military_time = False		#True:  Display as military time; False:  Display as am/pm.


# (10) VolpeV2 serial address:
#  Below is the VolpeV2 board serial address:

SERIALPORT = "/dev/ttyACM0"		#This is your Volpe board address.  The address entered at left is usually the default address, if you have only one board.


# (11) Power relays:
#  The following two lines routes where a power relay is when connected to a Raspberry Pi -- if applicable:

using_relay = 0			#If you are using a 5V power relay board on a Raspberry Pi, set the number at the end of this line to 1; 0 if no relay is being used.
relay_GPIO_pin = 17		#The number at the end of this line is the GPIO pin number on your Raspberry Pi, if using a relay.  Ignore this line if no relay is used.


# (12) Mac debugging:
#  The line below relates to debugging on a Mac computer... it should almost always be set to 0:

mac = 0		# Set to 1 if running on a Mac to test these scripts... otherwise keep at 0.


# Enjoy!!!