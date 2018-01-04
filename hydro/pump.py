from hydro.relay import Relay
import RPi.GPIO as GPIO
from background_task import background
import time

class Pump:
    def __init__(self):
        # set up GPIO using BCM numbering
        GPIO.setmode(GPIO.BOARD)

        self.peri_pump1 = Relay(11)
        self.peri_pump2 = Relay(13)
        self.peri_pump3 = Relay(15)

        self.dump_valve = Relay(29)
        self.water_valve = Relay(31)
        self.nutrients_valve = Relay(33)

        self.main_pump_forward = Relay(16)
        self.main_pump_back = Relay(18)

        self.pumping = False
        self.start_pump()

    @background(queue='pump_queue')
    def increase_pH(self, volume):
        self.stop_pump()

        pulse_length = volume / .1 * 60 #pumps at .1 L/min
        self.peri_pump1.pulse_on(pulse_length)

        self.start_pump()

    @background(queue='pump_queue')
    def decrease_pH(self, volume):
        self.stop_pump()

        pulse_length = volume / .1 * 60 #pumps at .1 L/min
        self.peri_pump2.pulse_on(pulse_length)

        self.start_pump()

    @background(queue='pump_queue')
    def increase_nutrients(self, volume):
        self.stop_pump()

        pulse_length = volume / .1 * 60 #pumps at .1 L/min
        self.peri_pump3.pulse_on(pulse_length)

        self.start_pump()

    @background(queue='pump_queue')
    def refill(self, volume):
        self.stop_pump()

        self.water_valve.activate()

        pulse_length = volume / 4.5 * 60 #pumps at 4.5 L/min
        self.main_pump_back.pulse_on(pulse_length)

        self.water_valve.deactivate()

        self.start_pump()

    @background(queue='pump_queue')
    def dump(self, resevoir_volume, basin_volume):
        self.stop_pump()

        self.dump_valve.activate()

        pulse_length = resevoir_volume / 4.5 * 60 #pumps at 4.5 L/min
        self.main_pump_forward.pulse_on(pulse_length)

        pulse_length = basin_volume / 4.5 * 60  #pumps at ? L/min
        self.nutrients_valve.pulse_on(pulse_length)

        self.dump_valve.deactivate()

        self.start_pump()

    def start_pump(self):
        if not self.pumping:
            time.sleep(1) #add buffer between tasks
            self.nutrients_valve.activate()

            self.main_pump_forward.activate()

    def stop_pump(self):
        if self.pumping:
            self.main_pump_forward.deactivate()

            self.nutrients_valve.deactivate()
            time.sleep(1) #add buffer between tasks

