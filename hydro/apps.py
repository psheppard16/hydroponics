from django.apps import AppConfig
from django.core import management
import datetime
import threading
from subprocess import check_output, PIPE
import subprocess
import time

class HydroConfig(AppConfig):
    name = 'hydro'
    verbose_name = 'Hydroponics Application'

    def ready(self):
        if False:
            from hydro.models import Data, DataType, Configuration
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

            def collect_data():
                pH = sensor.get_pH()
                if pH:
                    Data(date_time=datetime.datetime.now(), type=DataType(type="pH"), value=pH).save()
                EC = sensor.get_EC()
                if EC:
                    Data(date_time=datetime.datetime.now(), type=DataType(type="EC"), value=EC).save()
                ORP = sensor.get_ORP()
                if ORP:
                    Data(date_time=datetime.datetime.now(), type=DataType(type="ORP"), value=ORP).save()

            def monitor_data():
                config = Configuration.objects.get(id=1)

                delta = datetime.timedelta(seconds=config.polling_range)
                start = datetime.datetime.now() - delta
                end = datetime.datetime.now()

                change_interval = datetime.timedelta(seconds=config.min_change_interval)

                if config.auto_regulate_pH:
                    # Ph
                    can_change_pH = config.last_pH_change + change_interval < datetime.datetime.now()
                    if can_change_pH:
                        avg_pH = average_range("pH", start, end, config.minimun_data_count)
                        if avg_pH:
                            if avg_pH < config.low_pH:
                                pump.increase_pH(config.pH_adj_volume)
                            elif avg_pH > config.high_pH:
                                pump.increase_pH(config.pH_adj_volume)

                if config.auto_regulate_nutrients:
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
                        pump.water_change(config.basin_volume, config.resevoir_volume)
                    elif can_water_change:
                        avg_ORP = average_range("ORP", start, end, config.minimun_data_count)
                        if avg_ORP:
                            if avg_ORP < config.low_ORP:
                                pump.water_change(config.basin_volume, config.resevoir_volume)
                            elif avg_ORP > config.high_ORP:
                                pump.water_change(config.basin_volume, config.resevoir_volume)

            def run():
                while(server_alive()):
                    time.sleep(1)
                    collect_data()
                    monitor_data()

            def queue():
                while(server_alive()):
                    pump.queue.next()
                pump.reset_all()

            def server_alive():
                p = subprocess.Popen(["apachectl", "status"], stdin=PIPE, stdout=PIPE, stderr=PIPE)
                return "Unable to connect to remote host" not in str(p.communicate(timeout=1)[1])

            pump.increase_pH(1)
            pump.decrease_pH(1)
            pump.increase_nutrients(1)
            pump.refill(1)
            pump.water_change(90, 90)

            run_thread = threading.Thread(target=run)
            run_thread.setDaemon(True)
            run_thread.start()

            queue_thread = threading.Thread(target=queue)
            queue_thread.setDaemon(True)
            queue_thread.start()




