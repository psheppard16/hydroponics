import RPi.GPIO as GPIO
from hydro.relay import Relay
from django.apps import apps

def ready():
    print("wagfwagawggw")

    # #set up GPIO using BCM numbering
    # GPIO.setmode(GPIO.BOARD)
    # periPump1 = Relay(35)
    # periPump1.pulse_on(5)
    # GPIO.cleanup()