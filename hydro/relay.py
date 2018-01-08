import RPi.GPIO as GPIO
import time
class Relay:
    def __init__(self, pin, off_mode=True, mode=GPIO.OUT):
        GPIO.setup(pin, mode)
        self.pin = pin
        self.mode = mode
        self.active = False
        self.off_mode = off_mode
        self.reset()

    def activate(self):
        if self.active:
            raise Exception("already active")
        self.active = True
        GPIO.output(self.pin, not self.off_mode)

    def deactivate(self):
        if not self.active:
            raise Exception("already inactive")
        self.active = False
        GPIO.output(self.pin, self.off_mode)

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

    def reset(self):
        GPIO.output(self.pin, self.off_mode)
