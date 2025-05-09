import os, requests, threading, time, math, textwrap
from datetime import datetime, timedelta
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from settings import *
from TT_port import print_data
from dateutil import tz   #sudo apt install python3-dateutil
from dateutil.parser import *
from settings import APIKey

if not mac:
    from RelayOn import turn_on_relay
    from RelayOff import turn_off_relay
import gc


now = datetime.now()
wrapper = textwrap.TextWrapper(width=65)
wrapper_small = textwrap.TextWrapper(width=25)
wrapper_medium = textwrap.TextWrapper(width=48)
wrapper_indent = textwrap.TextWrapper(width=62, initial_indent='   ', subsequent_indent='   ')
current_hour = -1
relay_is_on = False

days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
alerts = []
new_data = False
try:
    log_alerts
except:
    log_alerts = True

try:
    headline_display
except:
    headline_display = False

s = requests.Session()
retries = Retry(total=math.inf,
                backoff_factor=1.5,
                status_forcelist=[ 101, 204, 205, 401, 404, 410, 444, 425, 429, 408, 500, 501, 502, 503, 504, 511, 520, 522, 524 ])
s.mount('https://', HTTPAdapter(max_retries=retries))


def garbage():
    time.sleep(0.5)
    gc.collect(generation=2)
    time.sleep(0.5)
    run_at = now + timedelta(minutes=45)  #Increase the frequency of garbage collection - if needed, here.
    delay = (run_at - now).total_seconds()
    print("\nFreeing memory (generation 2)\n")
    threading.Timer(delay, garbage).start()


print("\nStart Time: ",datetime.now(), "\n", flush=False)


def break_string(string):
    final_string = wrapper.fill(string)
    return final_string


def PrettyTime(datetime_value):
    if military_time:
        returnstring = datetime_value.strftime('%Y-%m-%d %-H:%M:%S')
    else:
        if datetime_value.strftime('%Z') == '':
            returnstring = datetime_value.strftime('%-I:%M%p local time %-m-%-d-%-Y')
        else:
            returnstring = datetime_value.strftime('%-I:%M%p %Z %-m-%-d-%-Y')
    return returnstring


def Datetimestring_to_datetime(datetime_string):
    return parse(datetime_string)


def Convert_Datestring_To_Timezone(datetime_string, timezone):
    datetime_value = Datetimestring_to_datetime(datetime_string)
    if(timezone):
        new__timezone = tz.gettz(timezone)
        datetime_value = datetime_value.astimezone(new__timezone)
    return PrettyTime(datetime_value)


def check_conditions(api_key=None):
    text = ""
    try:
        for location in conditions_and_forecast_locations:
            if location in conditions_and_forecast_locations is not None:
                global Cchecked
                if not Cchecked:
                    try:
                        station = location[0]
                        headers = {}
                        if api_key:   #NWS API key is needed -- see readme.
                            headers = {
                                "X-RapidAPI-Host": "api.weather.gov",
                                "X-RapidAPI-Key": api_key
                            }
                        station_url = "https://api.weather.gov/stations/" + station + "/observations/latest"
                        if station_url == "https://api.weather.gov/stations//observations/latest":
                            print("\nStand by...\n")
                            time.sleep(3.7)
                            continue
                        response = requests.get(station_url, headers=headers)
                        response.raise_for_status()
                        print("\nChecking if station" ,station, "is valid -- stand by...\n"  ,datetime.now().time(), "\n")
                        time.sleep(3.7)
                    except requests.exceptions.RequestException:
                        print(f"\nInvalid station(s):  A stations as entered either does not exist or doesn't allow for hourly observations (likely the above station code).\n"
                            "Please double check that you have the correct station code(s) entered in the conditions_and_forecast_locations section of the settings file.\n"
                            "This script will now terminate.\n"  ,datetime.now().time())
                        if using_relay:
                            if relay_is_on:
                                turn_off_relay(relay_is_on)
                        try:
                            gc.collect()
                        finally:
                            os._exit(1)
    finally:
        Cchecked = True    
Cchecked = False


def check_forecasts(api_key=None):
    text = ""
    try:
        for location in conditions_and_forecast_locations:
            if location in conditions_and_forecast_locations is not None:
                global Fchecked
                if not Fchecked:
                    try:
                        lat_lon = location[1]
                        headers = {}
                        if api_key:
                            headers = {
                                "X-RapidAPI-Host": "api.weather.gov",
                                "X-RapidAPI-Key": api_key
                            }
                        try:
                            forecast_url = ("https://api.weather.gov/points/{},{}".format(lat_lon[0], lat_lon[1]))
                        except:
                            continue
                        response = requests.get(forecast_url, headers=headers)
                        response.raise_for_status()
                        print("\nChecking if coordinates" ,lat_lon[0], lat_lon[1], "are vaild -- stand by...\n"  ,datetime.now().time(), "\n")
                        time.sleep(3.7)
                    except requests.exceptions.RequestException:
                        print(f"\nInvalid coordinates:  The coordinates provided are either incorrectly entered or are out of range (likely the above coordinates).\n"
                            "Please double check that you have the correct coordinates in the conditions_and_forecast_locations section of the settings file\n"
                            "and that they are entered in the following format (as exampled):  40.8312169,-96.7631597 .\n"
                            "This script will now terminate.\n"  ,datetime.now().time())
                        if using_relay:
                            if relay_is_on:
                                turn_off_relay(relay_is_on)
                        try:
                            gc.collect()
                        finally:
                            os._exit(1)
    finally:
        Fchecked = True    
Fchecked = False


def check_alerts(api_key=None):
    global Achecked
    if not Achecked:
        try:
            for area_or_zone in alert_locations:
                headers = {}
                if api_key:
                    headers = {
                        "X-RapidAPI-Host": "api.weather.gov",
                        "X-RapidAPI-Key": api_key
                    }
                alert_url = ("https://api.weather.gov/alerts/active/" + area_or_zone[1] + "/" + area_or_zone[0])
                response = requests.get(alert_url, headers=headers)
                response.raise_for_status()
                print("\nChecking if alert code" ,area_or_zone[0], "is valid -- stand by...\n"  ,datetime.now().time(), "\n")
                time.sleep(3.7)
        except requests.exceptions.RequestException:
            print(f"\nInvalid zone(s) or area(s):  A zone or area as entered does not exist (likely the above zone or area alert code).\n"
                "Please double check the zone/area codes in the alert_locations section of the settings file\n"
                "and that they are entered in the following format (alpha/numeric, as exampled):  ABC123 for zone or XX for area.\n"
                "This script will now terminate.\n"  ,datetime.now().time())
            if using_relay:
                if relay_is_on:
                    turn_off_relay(relay_is_on)
            try:
                gc.collect()
            finally:
                os._exit(1)
        finally:
            Achecked = True    
Achecked = False


def conditions_and_forecast(station_id, lat_lon, print_conditions, print_forecasts, api_key=None):
    text = ""
    if print_conditions:
        check_conditions()
        if station_id != "":
            url = "https://api.weather.gov/stations/" + station_id + "/observations/latest"
            observation = s.get(url,
                headers={
                    "X-RapidAPI-Host": "api.weather.gov",
                    "X-RapidAPI-Key": APIKey
                    }).json()["properties"]
            url = observation["station"]
            station = s.get(url,
                headers={
                    "X-RapidAPI-Host": "api.weather.gov",
                    "X-RapidAPI-Key": APIKey
                    }).json()["properties"]

            station_name = station["name"]
            station_timezone = station['timeZone']

            session = requests.Session()
            headers = {}
            station_url = f"https://api.weather.gov/stations/{station_id}"
            station_response = s.get(station_url, headers=headers).json()
            forecast_url = station_response.get("properties", {}).get("forecast", None)
            if not forecast_url:
                print(f"Forecast URL not found for station {station_id}")
            forecast_response = session.get(forecast_url, headers=headers).json()
            cwa = forecast_response.get("properties", {}).get("cwa", None)
            if not cwa:
                print("CWA not found for forecast zone {forecast_url}")
                
            forecast_office = "National Weather Service WFO-{}".format(cwa)
            
            lineWFOc = forecast_office.replace("'", "")
            text += "{}".format(lineWFOc)
            lineOB = wrapper.fill(" Current observations at...{} ({})...".format(station_name, station_id))
            
            if observation['timestamp'] != '':
                OBtz = Convert_Datestring_To_Timezone(observation['timestamp'], station_timezone)
                OBts = "{}".format(observation['textDescription'])
            text = "\n" + "Local Area Weather Roundup\n" + lineWFOc + "\n" + PrettyTime(datetime.now()) + "\n\n" + lineOB + "\n\n" + wrapper.fill("At " + OBtz + ", it/there was..." + OBts + "...")   
                
            try:
                if observation["temperature"]["value"] != None:
                    if observation["temperature"]["unitCode"] == "wmoUnit:degC":
                        centigrade = round(observation["temperature"]["value"], 1)
                        farenheit = round(9/5*centigrade + 32, 1)
                        centigrade_r = round(centigrade)
                        farenheit_r = round(farenheit)
                        text += "\n   Temperature...{}F ({}C)".format(farenheit_r, centigrade_r)
            except:
                print("bad value from api for temperature.", observation["temperature"]["value"] )
                
            if observation["relativeHumidity"]["value"] != None:
                text += "\n   Relative humidity...{} percent".format(round(observation["relativeHumidity"]["value"]))
                
            try:
                if observation["windSpeed"]["value"] != None:
                    if observation["windDirection"]["value"] != None:
                        dirs = ['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE', 'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW',
                                'NNW']
                        ix = round(observation["windDirection"]["value"] / (360. / len(dirs)))
                        direction = dirs[ix % len(dirs)]
                        text += "\n   Wind...{} ".format(direction)
                    speed = round(observation["windSpeed"]["value"] / 1.609344)
                    if observation["windSpeed"]["unitCode"] == "wmoUnit:km_h-1":
                        text += "{}".format(speed) 
            except:
                print("bad value from api for windSpeed:", observation["windSpeed"]["value"] )
            
            try:
                if observation["windGust"]["value"] != None:
                    if observation["windGust"]["unitCode"] == "wmoUnit:km_h-1":
                        gust = round(observation["windGust"]["value"] / 1.609344)
                        text += ", gusting to {} MPH".format(gust)
                elif observation["windSpeed"]["value"] is None:
                    text += ""
                else:
                    text += " MPH"
                    
            except:
                print("bad value from api for windGust:", observation["windGust"]["value"] )
                
            try:
                if observation["elevation"]["value"] != None:
                    if observation["elevation"]["unitCode"] == "wmoUnit:m":
                        elevation = observation["elevation"]["value"]* 3.28084
                        if observation["barometricPressure"]["value"] != None:
                            if observation["barometricPressure"]["unitCode"] == "wmoUnit:Pa":
                                pressure = observation["barometricPressure"]["value"] / 3386.389
                                adjust = elevation * .001  #.01 inHg per 10 feet elevation
                                text += "\n   Barometer...{:0.2f} IN".format(round(pressure, 2))
                                text += " ({:0.2f} at station)".format(round(pressure-adjust, 2))
            except:
                print("bad value from api for elevation:", observation["elevation"]["value"],"or barometricPressure", observation["barometricPressure"]["value"] )

            try:
                if observation["dewpoint"]["value"] != None:
                    if observation["dewpoint"]["unitCode"] == "wmoUnit:degC":
                        centigrade = round(observation["dewpoint"]["value"], 1)
                        farenheit = round(9 / 5 * centigrade + 32, 1)
                        centigrade_r = round(centigrade)
                        farenheit_r = round(farenheit)
                        text += "\n   Dewpoint...{}F ({}C)".format(farenheit_r, centigrade_r)
            except:
                print("bad value from api for dewpoint:", observation["dewpoint"]["value"] )

            try:
                if observation["visibility"]["value"] != None:
                    if observation["visibility"]["unitCode"] == "wmoUnit:m":
                        visibility = round(observation["visibility"]["value"] / 1609.3)
                        text += "\n   Visibility...{} MI".format(visibility)
            except:
                print("bad value from api for visibility:", observation["visibility"]["value"])

            try:
                if observation["windChill"]["value"] != None:
                    if observation["windChill"]["unitCode"] == "wmoUnit:degC":
                        centigrade = round(observation["windChill"]["value"], 1)
                        farenheit = round(9 / 5 * centigrade + 32, 1)
                        centigrade_r = round(centigrade)
                        farenheit_r = round(farenheit)
                        text += "\n   Wind Chill...{}F ({}C)".format(farenheit_r, centigrade_r)
                else:
                    if observation["heatIndex"]["value"] != None:
                        if observation["heatIndex"]["unitCode"] == "wmoUnit:degC":
                            centigrade = round(observation["heatIndex"]["value"], 0)
                            farenheit = round(9 / 5 * centigrade + 32, 0)
                            centigrade_r = round(centigrade)
                            farenheit_r = round(farenheit)
                            text += "\n   Heat Index...{}F ({}C)".format(farenheit_r, centigrade_r)
            except:
                print("bad value from api for heat index:", observation["heatIndex"]["value"],"or wind chill", observation["windCill"]["value"] )

            text += "\n   Elevation...{} FEET".format(round(elevation))
         
            text += "\n\n" + wrapper_medium.fill(observation["rawMessage"]) + "\n"
            

    if print_forecasts:
        check_forecasts()
        if len(lat_lon) == 2:
            url = "https://api.weather.gov/points/{},{}".format(lat_lon[0], lat_lon[1])
            points = s.get(url,
                headers={
                    "X-RapidAPI-Host": "api.weather.gov",
                    "X-RapidAPI-Key": APIKey
                    }).json()["properties"]

            url = points["forecastZone"]
            zone = s.get(url,
                headers={
                    "X-RapidAPI-Host": "api.weather.gov",
                    "X-RapidAPI-Key": APIKey
                    }).json()["properties"]
            zonetimezone = zone['timeZone'][0]

            url = points["forecast"]
            forecast = s.get(url,
                headers={
                    "X-RapidAPI-Host": "api.weather.gov",
                    "X-RapidAPI-Key": APIKey
                    }).json()["properties"]
            
            url = points["forecastOffice"]
            forecastOffice = s.get(url,
                headers={
                    "X-RapidAPI-Host": "api.weather.gov",
                    "X-RapidAPI-Key": APIKey
                    }).json()["id"]

            lineF = wrapper.fill("{}, {} ({}) and vicinity forecast".format(zone["name"], zone["state"], zone["id"])) + "\n"

            datestring = forecast['updateTime']
            datestring = Convert_Datestring_To_Timezone(datestring, zonetimezone)
        
            lineWFOf = "National Weather Service WFO-{}".format(forecastOffice)
            
            text += "\n"
            text += lineF
            text += lineWFOf + "\nIssued/updated {}".format(datestring)
            
            number_to_print = min(number_of_forecast_periods, len(forecast["periods"]))
            for i in range(number_to_print):
                period = forecast["periods"][i]
                text += "\n\n {}...\n".format(period["name"])
                detailed_forecast = (wrapper_indent.fill(period["detailedForecast"]))
                detailed_forecast_C1 = detailed_forecast.replace(". ", ".  ")
                detailed_forecast_C2 = detailed_forecast_C1.replace("%", " percent")
                text += "{}".format(detailed_forecast_C2)
            text += "\n"
    return text


def dump_properties(element, all=False):
    if not all:
        items = ['id', 'sent', 'effective', 'expires', 'ends', 'status', 'messageType', 'event']
        for item in items:
            properties = element['properties']
            try:
                print(item+":", properties[item])
            except:
                print(item + ":", "Not found")
    else:
        properties = element['properties']
        for property in properties:
            print(property+":", properties[property])
    print("\n\n")


def scrape_alerts():
    if log_alerts:
        print("\nChecking (for) alerts...\n"  ,datetime.now().time(), "\n")
    global alerts
    temp = []
    for area_or_zone in alert_locations:        
        url = "https://api.weather.gov/alerts/active/" + area_or_zone[1] + "/" + area_or_zone[0]

        api_data = s.get(url,
        headers={
            "X-RapidAPI-Host": "api.weather.gov",
            "X-RapidAPI-Key": APIKey
            }).json()["features"]

        for new_dict in api_data:
            temp_dict = {}
            temp_dict['id'] = new_dict['properties']['id']
            temp_dict['sent'] = Convert_Datestring_To_Timezone(new_dict['properties']['sent'], None)
            temp_dict['event'] = new_dict['properties']['event']
            temp_dict['headline'] = new_dict['properties']['headline']
            if log_alerts:
                print(new_dict['properties']['event'])
            temp_dict['sendername'] = new_dict['properties']['senderName']
            temp_dict['description'] = new_dict['properties']['description']
            temp_dict['instruction'] = new_dict['properties']['instruction']
            temp_dict['areadesc'] = new_dict['properties']['areaDesc']
            if temp_dict in alerts:
                temp_dict["type"] = "old"
            else:
                temp_dict["type"] = "new"
                global new_data
                new_data = True
            temp.append(temp_dict)        
    alerts = temp


def printit(data, num, type):
    print("\nPrinting", type, "on Teletype at",datetime.now().time(), "\n")
    if mac:
        print(data)
    if len(SERIALPORT) > 0:
        print_data(data, num)
    print("\nPrintout complete on Teletype at",datetime.now().time(), "\n")


def prepare_text(data, type):
    text = wrapper_small.fill("{0}".format(data['id'])) + "\n\n"

    if type == "warning" or type == "watch":
        text += "ZZZZZ\n\n"
        text += "Bulletin\n"
    else:
        text += "Urgent\n"
    if headline_display:
        text += wrapper.fill("{0}".format(data['headline']))
        text += "\n\n"
    else:
        text += "{0}\n".format(data['event'])
        text += "{0}\n\n".format(data['sendername'])
        text += "Issued "
        text += "{0}\n\n".format(data['sent'])
        
    data['description']
    description = data['description']
    description_C1 = description.replace(". ", ".  ")
    description_C2 = description_C1.replace("%", " percent")
    description_C3 = description_C2.replace("* WHAT...", " ..WHAT...")
    description_C4 = description_C3.replace("* WHERE...", " ..WHERE...")
    description_C5 = description_C4.replace("* WHEN...", " ..WHEN...")
    description_C6 = description_C5.replace("* IMPACTS...", " ..IMPACTS...")
    description_C7 = description_C6.replace("* ADDITIONAL DETAILS...", " ..ADDITIONAL DETAILS...")
    
    text += "{0}\n\n".format(description_C7)
    
    if data['instruction'] is not None:
        instruction = data['instruction']
        instruction_C1 = instruction.replace(". ", ".  ")
        instruction_C2 = instruction_C1.replace("%", " percent")
        text += "{0}\n\n".format(instruction_C2)
        
    areas_text = break_string(data['areadesc'])
    areas_text1 = areas_text.replace(";", ",")
    text += " Counties/locations include...\n{0}.\n".format(areas_text1)
    return text


def convert_to_string(data):
    if "warning" in data['event'].lower():
        bells = 10
        text = prepare_text(data, "warning")
    elif "watch" in data['event'].lower():
        bells = 5
        text = prepare_text(data, "watch")
    else:
        bells = 4
        text = prepare_text(data, "")
    final_output = "\nZCZC\n"+text+"NNNN\n\n\n"
    return final_output, bells


def ok_to_print(the_time, dictionary):
    day = days_of_week[the_time.weekday()]
    hour = the_time.hour
    return hour in dictionary[day]


try:
    garbage()
    while True:
        final_output = ""
        current_time = datetime.now()
        hour = current_time.hour
        if hour not in quiet_hours:
            check_alerts()
            if hour != current_hour:
                current_hour = hour
                print_conditions = ok_to_print(current_time, days_hours_conditions)
                print_forecasts = ok_to_print(current_time, days_hours_forecasts)
                
                if print_conditions or print_forecasts:
                    for location in conditions_and_forecast_locations:
                        station = location[0]
                        lat_lon = location[1]
                        final_output += conditions_and_forecast(station, lat_lon, print_conditions, print_forecasts)
                    if len(final_output)>0:
                        final_output = "\n\nZCZC" + final_output + "NNNN\n\n\n"
                        if using_relay:
                            relay_is_on = turn_on_relay(relay_is_on)
                            time.sleep(7.0)

                        printit(final_output, 0, "conditions and/or forecasts")
                        time.sleep(10.0)
                        
            scrape_alerts()
            if new_data:
                if using_relay:
                    relay_is_on = turn_on_relay(relay_is_on)
                    time.sleep(7.0)
                while new_data:
                    for data in alerts:
                        if data["type"] == "new":
                            text, bells = convert_to_string(data)
                            printit(text, bells, "alert")
                    new_data = False
                    alerts = [{k: v for k, v in alert.items() if k != 'type'} for alert in alerts]
                    scrape_alerts()
                time.sleep(5.0)

            alerts = [{k: v for k, v in alert.items() if k != 'type'} for alert in alerts]
        else:
            if hour != current_hour:
                current_hour = hour
                print("Hour {} is in quiet hours, not checking/printing".format(hour))
        if using_relay:
            relay_is_on = turn_off_relay(relay_is_on)
        new_data = False
        time.sleep(sleeptime)


except Exception as e:
    print("\nThere has been a fatal error (please see below).  This script will now terminate.\n")
    print("Exit Time: ",datetime.now(), "\n")
    print(e, "\n")
    if using_relay:
        if relay_is_on:
            turn_off_relay(relay_is_on)
        try:
            gc.collect()
        finally:
            os._exit(1)