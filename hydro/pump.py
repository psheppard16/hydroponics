from hydro.relay import Relay
import RPi.GPIO as GPIO
import time

class Pump:
    def __init__(self):
        # set up GPIO using BCM numbering
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)

        self.peri_pump1 = Relay(3)
        self.peri_pump2 = Relay(5)
        self.peri_pump3 = Relay(7)

        self.water_change_valve = Relay(11)
        self.water_valve = Relay(13)
        self.nutrients_valve = Relay(15)

        self.main_valve = Relay(19)
        self.main_pump = Relay(21)

        self.pumping = False

    def reset_all(self):
        self.peri_pump1.reset()
        self.peri_pump2.reset()
        self.peri_pump3.reset()

        self.water_change_valve.reset()
        self.water_valve.reset()
        self.nutrients_valve.reset()

        self.main_valve.reset()
        self.main_pump.reset()

    def increase_pH(self, volume):
        pulse_length = volume / 100 * 60 #pumps at 100 mL/min
        self.peri_pump1.pulse_on(pulse_length)

    def decrease_pH(self, volume):
        pulse_length = volume / 100 * 60 #pumps at 100 mL/min
        self.peri_pump2.pulse_on(pulse_length)

    def increase_nutrients(self, volume):
        pulse_length = volume / 100 * 60 #pumps at 100 mL/min
        self.peri_pump3.pulse_on(pulse_length)

    def refill(self, volume):
        self.main_valve.activate()
        self.water_valve.activate()

        pulse_length = volume / 4.5 * 60 #pumps at 4.5 L/min
        self.main_pump.pulse_on(pulse_length)

        self.water_valve.deactivate()
        self.main_valve.deactivate()

    def water_change(self, resevoir_volume, basin_volume):
        self.water_change_valve.activate()
        self.water_valve.activate()

        pulse_length = resevoir_volume / 4.5 * 60 #pumps at 4.5 L/min
        self.main_pump.pulse_on(pulse_length)

        pulse_length = basin_volume / 4.5 * 60  #pumps at ? L/min
        self.nutrients_valve.pulse_on(pulse_length)

        self.water_change_valve.deactivate()
        self.water_valve.deactivate()

    def start_pump(self):
        if self.pumping:
            raise Exception("Already pumping")
        time.sleep(1) #add buffer between tasks
        self.pumping = True

        self.main_valve.activate()
        self.nutrients_valve.activate()
        self.main_pump.activate()

    def stop_pump(self):
        if not self.pumping:
            raise Exception("Already not pumping")
        self.main_pump.deactivate()
        self.nutrients_valve.deactivate()
        self.main_valve.deactivate()

        self.pumping = False
        time.sleep(1) #add buffer between tasks