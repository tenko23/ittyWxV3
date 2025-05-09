import RPi.GPIO as GPIO
from datetime import datetime
from  settings import *

GPIO.setwarnings(False)

def turn_off_relay(relay_is_on):
    if relay_is_on:
        GPIO.setmode(GPIO.BCM)
        RELAIS_1_GPIO = relay_GPIO_pin
        GPIO.setup(RELAIS_1_GPIO, GPIO.OUT)
        GPIO.output(RELAIS_1_GPIO, GPIO.LOW)
        print("\nTurning off relay at",datetime.now().time(), "\n")
        GPIO.cleanup()
    return False
