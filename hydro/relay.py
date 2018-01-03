import RPi.GPIO as GPIO
import time
class Relay:
    def __init__(self, pin, mode=GPIO.OUT):
        GPIO.setup(pin, mode)
        self.pin = pin
        self.mode = mode
        self.active = False

    def activate(self):
        if self.active:
            raise Exception("already active")
        self.active = True
        GPIO.output(self.pin, True)

    def deactivate(self):
        if not self.active:
            raise Exception("already inactive")
        self.active = False
        GPIO.output(self.pin, False)

    def pulse_on(self, wait):
        if self.active:
            raise Exception("already active")
        self.activate()
        time.sleep(wait)
        self.deactivate()

    def pulse_off(self, wait):
        if not self.active:
            raise Exception("already inactive")
        self.deactivate()
        time.sleep(wait)
        self.activate()

