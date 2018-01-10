from django.apps import AppConfig
import django.utils.timezone as tz
import threading
from subprocess import PIPE
import subprocess
import datetime
import time
import logging


log = logging.getLogger('hydro')

class HydroConfig(AppConfig):
    name = 'hydro'
    verbose_name = 'Hydroponics Application'

    def ready(self):
        if True:
            from hydro.models import Data, DataType, Configuration, Request, RequestType, Status
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
                log.info("Collecting data")
                pH = sensor.get_pH()
                if pH:
                    Data(date_time=tz.now(), type=DataType(type="pH"), value=pH).save()
                EC = sensor.get_EC()
                if EC:
                    Data(date_time=tz.now(), type=DataType(type="EC"), value=EC).save()
                ORP = sensor.get_ORP()
                if ORP:
                    Data(date_time=tz.now(), type=DataType(type="ORP"), value=ORP).save()

            def monitor_data():
                log.info("Monitoring data")
                config = Configuration.objects.get(id=1)

                delta = datetime.timedelta(seconds=config.polling_range)
                start = tz.now() - delta
                end = tz.now()

                change_interval = datetime.timedelta(seconds=config.min_change_interval)

                if config.auto_regulate_pH:
                    # Ph
                    can_change_pH = config.last_pH_change + change_interval < tz.now()
                    if can_change_pH:
                        avg_pH = average_range("pH", start, end, config.minimun_data_count)
                        if avg_pH:
                            if avg_pH < config.low_pH:
                                pump.increase_pH(config.pH_adj_volume)
                            elif avg_pH > config.high_pH:
                                pump.increase_pH(config.pH_adj_volume)

                if config.auto_regulate_nutrients:
                    # EC
                    can_change_EC = config.last_EC_change + change_interval < tz.now()
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
                    can_water_change = config.last_water_change + min_water_change_interval < tz.now()
                    must_water_change = config.last_water_change + max_water_change_interval > tz.now()
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
                log.info("Starting run loop")

                while(server_alive()):
                    time.sleep(1)
                    # collect_data()
                    # monitor_data()

                log.info("Exiting run loop")

            def queue():
                log.info("Starting queue loop")

                log.info("Canceling unfinished requests")
                requested = Request.objects.filter(status=Status.objects.get(status="requested"))
                requested.update(status=Status.objects.get(status="canceled"))

                log.info("Initializing pump")


                while(server_alive()):
                    unhandled = Request.objects.filter(status=Status.objects.get(status="requested"))
                    if unhandled:
                        next = unhandled.order_by('request_time')[0]
                        log.info("Attempting request: " + str(next))

                        try:
                            function_name = str(next.type)
                            function = getattr(pump, function_name)

                            try:
                                if next.arg1 and next.arg2:
                                    function(float(next.arg1), float(next.arg2))
                                elif next.arg1:
                                    function(float(next.arg1))
                                else:
                                    function()
                                next.status = Status.objects.get(status="completed")
                                next.exec_time = tz.now()
                                next.save()
                            except Exception as e:
                                log.error("Failed to execute request. Error: " + str(e))
                                next.status = Status.objects.get(status="failed")
                                next.save()
                        except Exception as e:
                            log.error("Failed to parse request. Error: " + str(e))
                            next.status = Status.objects.get(status="failed")
                            next.save()

                pump.reset_all()
                log.info("Exiting queue loop")

            def server_alive():
                p = subprocess.Popen(["apachectl", "status"], stdin=PIPE, stdout=PIPE, stderr=PIPE)
                return "Unable to connect to remote host" not in str(p.communicate(timeout=1)[1])


            run_thread = threading.Thread(target=run)
            run_thread.setDaemon(True)
            run_thread.start()

            queue_thread = threading.Thread(target=queue)
            queue_thread.setDaemon(True)
            queue_thread.start()