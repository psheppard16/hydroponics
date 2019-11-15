from django.apps import AppConfig
import django.utils.timezone as tz
import threading
from subprocess import PIPE
import subprocess
import datetime
import time
import logging
from hydro.sensor import Sensor
from hydro.pump import Pump

log = logging.getLogger('hydro')


class HydroConfig(AppConfig):
    name = 'hydro'
    verbose_name = 'Hydroponics Application'

    def ready(self):
        # import here because apps need to be loaded for models to exist
        from hydro.models import Data, DataType, WasteSettings, ChemicalSettings, Request, RequestType, Status
        sensor = Sensor()
        pump = Pump()
        log.info("Starting...")

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
                Data(date_time=tz.now(), type=DataType.objects.get(type="pH"), value=pH).save()
            EC = sensor.get_EC()
            if EC:
                Data(date_time=tz.now(), type=DataType.objects.get(type="EC"), value=EC).save()
            ORP = sensor.get_ORP()
            if ORP:
                Data(date_time=tz.now(), type=DataType.objects.get(type="ORP"), value=ORP).save()

        def monitor_data():
            chemical = ChemicalSettings.objects.get(id=1)

            delta = datetime.timedelta(seconds=chemical.polling_range)
            start = tz.now() - delta
            end = tz.now()

            change_interval = datetime.timedelta(seconds=chemical.min_change_interval)

            if chemical.auto_regulate_pH:
                # Ph
                can_change_pH = chemical.last_pH_change + change_interval < tz.now()
                if can_change_pH:
                    avg_pH = average_range("pH", start, end, chemical.minimun_data_count)
                    if avg_pH:
                        if avg_pH < chemical.low_pH:
                            Request(type=RequestType.objects.get(type="increase_pH"), arg1=chemical.pH_adj_volume)
                        elif avg_pH > chemical.high_pH:
                            Request(type=RequestType.objects.get(type="decrease_pH"), arg1=chemical.pH_adj_volume)

            if chemical.auto_regulate_nutrients:
                # EC
                can_change_EC = chemical.last_EC_change + change_interval < tz.now()
                if can_change_EC:
                    avg_EC = average_range("EC", start, end, chemical.minimun_data_count)
                    if avg_EC:
                        if avg_EC < chemical.low_EC:
                            Request(type=RequestType.objects.get(type="increase_nutrients"),
                                    arg1=chemical.nutrient_adj_volume)
                        elif avg_EC > chemical.high_EC:
                            raise Exception("EC values above desired levels")

            if chemical.auto_water_change:
                # ORP
                max_water_change_interval = datetime.timedelta(days=chemical.maximum_water_change_interval)
                min_water_change_interval = datetime.timedelta(days=chemical.minimum_water_change_interval)
                can_water_change = chemical.last_water_change + min_water_change_interval < tz.now()
                must_water_change = chemical.last_water_change + max_water_change_interval > tz.now()
                if must_water_change:
                    Request(type=RequestType.objects.get(type="water_change"),
                            arg1=chemical.basin_volume, arg2=chemical.resevoir_volume)
                elif can_water_change:
                    avg_ORP = average_range("ORP", start, end, chemical.minimun_data_count)
                    if avg_ORP and (avg_ORP < chemical.low_ORP or avg_ORP > chemical.high_ORP):
                        Request(type=RequestType.objects.get(type="water_change"),
                                arg1=chemical.basin_volume, arg2=chemical.resevoir_volume)

        def run():
            log.info("Starting run loop")

            while server_alive():
                time.sleep(1)
                collect_data()
                # monitor_data()

            log.info("Exiting run loop")

        def queue():
            log.info("Starting queue loop")

            log.info("Canceling unfinished requests")
            requested = Request.objects.filter(status=Status.objects.get(status="requested"))
            requested.update(status=Status.objects.get(status="canceled"))

            log.info("Initializing pump")

            while server_alive():
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

        queue_thread = threading.Thread(target=queue)
        queue_thread.setDaemon(True)
        queue_thread.start()

        run_thread = threading.Thread(target=run)
        run_thread.setDaemon(True)
        run_thread.start()
