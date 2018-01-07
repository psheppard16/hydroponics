from django.core.management.base import BaseCommand, CommandError
from hydro.models import *

import logging
from django.utils import timezone
log = logging.getLogger('status')

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

        pH_type, created = Type.objects.update_or_create(id=1, defaults={"type": "pH"})
        EC_type, created = Type.objects.update_or_create(id=2, defaults={"type": "EC"})
        ORP_type, created = Type.objects.update_or_create(id=3, defaults={"type": "ORP"})

    log.info("Configuration complete")
