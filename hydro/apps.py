from django.apps import AppConfig
from django.core import management
import datetime

class HydroConfig(AppConfig):
    name = 'hydro'
    verbose_name = 'Hydroponics Application'

    def ready(self):
        if False:
            from background_task import background
            from hydro.models import Data, Type, Configuration
            from hydro.sensor import Sensor
            from hydro.pump import Pump
            pump = Pump()
            sensor = Sensor()

            def average_range(type, start_time, end_time, min):
                data = Data.objects.filter(type=type, datetime__gte=start_time, datetime__lte=end_time)
                if len(data) < min:
                    return None
                sum = 0
                for i in data:
                    sum += i.value
                return sum / len(data)

            @background
            def collect_data():
                pH = sensor.get_pH()
                if pH:
                    Data(date_time=datetime.datetime.now(), type=Type(type="pH"), value=pH).save()
                EC = sensor.get_EC()
                if EC:
                    Data(date_time=datetime.datetime.now(), type=Type(type="EC"), value=EC).save()
                ORP = sensor.get_ORP()
                if ORP:
                    Data(date_time=datetime.datetime.now(), type=Type(type="ORP"), value=ORP).save()

            @background
            def monitor_data():
                config = Configuration.objects.all.get()

                delta = datetime.timedelta(seconds=config.polling_range)
                start = datetime.datetime.now() - delta
                end = datetime.datetime.now()

                if config.auto_regulate:
                    change_interval = datetime.timedelta(seconds=config.min_change_interval)
                    # Ph
                    can_change_pH = config.last_pH_change + change_interval < datetime.datetime.now()
                    if can_change_pH:
                        avg_pH = average_range("pH", start, end, config.minimun_data_count)
                        if avg_pH:
                            if avg_pH < config.low_pH:
                                pump.increase_pH(config.pH_adj_volume)
                            elif avg_pH > config.high_pH:
                                pump.increase_pH(config.pH_adj_volume)

                    # EC
                    can_change_EC = config.last_EC_change + change_interval < datetime.datetime.now()
                    if can_change_EC:
                        avg_EC = average_range("EC", start, end, config.minimun_data_count)
                        if avg_EC:
                            if avg_EC < config.low_EC:
                                pump.increase_nutrients(config.nutrient_adj_volume)
                            elif avg_EC > config.high_EC:
                                raise Exception("EC values above desired levels")

                if config.auto_water_change:
                    # ORP
                    max_water_change_interval = datetime.timedelta(days=config.maximum_water_change_interval)
                    min_water_change_interval = datetime.timedelta(days=config.minimum_water_change_interval)
                    can_water_change = config.last_water_change + min_water_change_interval < datetime.datetime.now()
                    must_water_change = config.last_water_change + max_water_change_interval > datetime.datetime.now()
                    if must_water_change:
                        pump.water_change()
                    elif can_water_change:
                        avg_ORP = average_range("ORP", start, end, config.minimun_data_count)
                        if avg_ORP:
                            if avg_ORP < config.low_ORP:
                                pump.water_change()
                            elif avg_ORP > config.high_ORP:
                                pump.water_change()

            # collect data every second forever
            collect_data(repeat=1, repeat_until=None)

            # monitor data every second forever
            monitor_data(repeat=1, repeat_until=None)

            management.call_command('process_tasks', sleep=1)
        else:
            from background_task import background
            from hydro.models import Data, Type, Configuration
            # from hydro.sensor import Sensor #imports dont work for some reason
            # from hydro.pump import Pump
            from hydro.relay import Relay
            import RPi.GPIO as GPIO

            # set up GPIO using BCM numbering
            GPIO.setmode(GPIO.BOARD)
            GPIO.setwarnings(False)

            r1 = Relay(3)
            r2 = Relay(5)
            # r3 = Relay(7)
            # r4 = Relay(11)
            # r5 = Relay(13)
            # r6 = Relay(15)
            # r7 = Relay(19)
            # r8 = Relay(21)
            # relays = [r1, r2, r3, r4, r5, r6, r7, r8]
            #
            r1.pulse_on(3)
            r2.pulse_on(3)




