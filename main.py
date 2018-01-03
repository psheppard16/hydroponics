import RPi.GPIO as GPIO
from hydro.relay import Relay

if __name__ == '__main__':
    #set up GPIO using BCM numbering
    GPIO.setmode(GPIO.BOARD)
    periPump1 = Relay(35)
    periPump1.pulse_on(5)
    GPIO.cleanup()