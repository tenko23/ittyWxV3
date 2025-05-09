import RPi.GPIO as GPIO
from datetime import datetime
from settings import *

def turn_on_relay(relay_is_on):
    if not relay_is_on:
        GPIO.setmode(GPIO.BCM)
        RELAIS_1_GPIO = relay_GPIO_pin
        GPIO.setup(RELAIS_1_GPIO, GPIO.OUT)
        GPIO.output(RELAIS_1_GPIO, GPIO.LOW)
        GPIO.output(RELAIS_1_GPIO, GPIO.HIGH)
        print("\nTurning on relay at",datetime.now().time(), "\n")
    return True
