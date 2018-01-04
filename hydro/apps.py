import RPi.GPIO as GPIO
from hydro.relay import Relay
from django.apps import AppConfig

class HydroConfig(AppConfig):
    name = 'hydro'

    def ready(self):
        print("ready")
        print("ready")
        print("ready")
        print("ready")
        print("ready")

# #set up GPIO using BCM numbering
# GPIO.setmode(GPIO.BOARD)
# periPump1 = Relay(35)
# periPump1.pulse_on(5)
# GPIO.cleanup()