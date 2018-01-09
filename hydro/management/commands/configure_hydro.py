from django.core.management.base import BaseCommand, CommandError
from hydro.models import *

import logging
from django.utils import timezone
log = logging.getLogger('hydro')

class Command(BaseCommand):
    help = 'Configures models for the hydro application.'

    def handle(self, *args, **options):
        """Adds default entries for the hydro app.

		    :returns: None
			"""
        configuration, created = Configuration.objects.update_or_create(id=1,
		defaults={  "auto_regulate_pH": "False",
                    "low_pH": "5",
                    "high_pH": "7",
                    "pH_adj_volume": "1",
                    "last_pH_change": timezone.now(),
                    "auto_regulate_nutrients": "False",
                    "low_EC": "5",
                    "high_EC": "7",
                    "nutrient_adj_volume": "1",
                    "last_nutrient_change": timezone.now(),
                    "auto_water_change": "False",
                    "low_ORP": "5",
                    "high_ORP": "7",
                    "last_water_change": timezone.now(),
                    "maximum_water_change_interval": "30",
                    "minimum_water_change_interval": "1",
                    "auto_pump": "False",
                    "auto_refill": "False",
                    "resevoir_volume": "90",
                    "basin_volume": "90",
                    "min_change_interval": "2",
                    "polling_range": "1",
                    "minimun_data_count": "60"})

        pH, created = DataType.objects.update_or_create(id=1, defaults={"type": "pH"})
        EC, created = DataType.objects.update_or_create(id=2, defaults={"type": "EC"})
        ORP, created = DataType.objects.update_or_create(id=3, defaults={"type": "ORP"})

        requested, created = Status.objects.update_or_create(id=1, defaults={"status": "requested"})
        completed, created = Status.objects.update_or_create(id=2, defaults={"status": "completed"})
        canceled, created = Status.objects.update_or_create(id=3, defaults={"status": "canceled"})
        failed, created = Status.objects.update_or_create(id=3, defaults={"status": "failed"})

        increase_pH, created = RequestType.objects.update_or_create(id=1, defaults={"type": "increase_pH"})
        decrease_pH, created = RequestType.objects.update_or_create(id=2, defaults={"type": "decrease_pH"})
        increase_nutrients, created = RequestType.objects.update_or_create(id=3, defaults={"type": "increase_nutrients"})
        refill, created = RequestType.objects.update_or_create(id=3, defaults={"type": "refill"})
        water_change, created = RequestType.objects.update_or_create(id=3, defaults={"type": "water_change"})
        start_pump, created = RequestType.objects.update_or_create(id=3, defaults={"type": "start_pump"})
        stop_pump, created = RequestType.objects.update_or_create(id=3, defaults={"type": "stop_pump"})




    log.info("Configuration complete")
