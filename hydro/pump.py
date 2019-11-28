from hydro.relay import Relay
import RPi.GPIO as GPIO
import time


class Pump:
    def __init__(self):
        # set up GPIO using BCM numbering
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)

        self.peri_pump1 = Relay(8)
        self.peri_pump2 = Relay(10)
        self.peri_pump3 = Relay(12)
        self.peri_pump4 = Relay(16)

        self.clean_water_valve = Relay(18)
        self.dump_valve = Relay(22)
        self.nutrient_water_valve = Relay(24)
        self.main_pump_and_valve = Relay(26)

        self.pumping = False

    def reset_all(self):
        self.peri_pump1.reset()
        self.peri_pump2.reset()
        self.peri_pump3.reset()
        self.peri_pump4.reset()

        self.dump_valve.reset()
        self.clean_water_valve.reset()
        self.nutrient_water_valve.reset()

        self.main_pump_and_valve.reset()

    def increase_pH(self, volume):
        pulse_length = volume / 100 * 60  # pumps at 100 mL/min
        self.peri_pump1.pulse_on(pulse_length)

    def decrease_pH(self, volume):
        pulse_length = volume / 100 * 60  # pumps at 100 mL/min
        self.peri_pump2.pulse_on(pulse_length)

    def increase_nutrients(self, volume):
        pulse_length = volume / 100 * 60  # pumps at 100 mL/min
        self.peri_pump3.pulse_on(pulse_length)

    def refill(self, volume):
        self.clean_water_valve.activate()
        self.nutrient_water_valve.activate()

        pulse_length = volume / 4.5 * 60  # pumps at 4.5 L/min
        self.main_pump_and_valve.pulse_on(pulse_length)

        self.clean_water_valve.deactivate()
        self.nutrient_water_valve.deactivate()

    def water_change(self, resevoir_volume, basin_volume):
        self.dump_valve.activate()
        self.nutrient_water_valve.activate()

        pulse_length = resevoir_volume / 4.5 * 60  # pumps at 4.5 L/min
        self.main_pump_and_valve.pulse_on(pulse_length)

        self.nutrient_water_valve.deactivate()
        self.dump_valve.deactivate()

    def start_pump(self):
        if self.pumping:
            raise Exception("Already pumping")
        time.sleep(1)  # add buffer between tasks
        self.pumping = True

        self.main_pump_and_valve.activate()
        self.nutrient_water_valve.activate()

    def stop_pump(self):
        if not self.pumping:
            raise Exception("Already not pumping")
        self.main_pump_and_valve.deactivate()
        self.nutrient_water_valve.deactivate()

        self.pumping = False
        time.sleep(1)  # add buffer between tasks
