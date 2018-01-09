from django.core.management.base import BaseCommand, CommandError
import os, webbrowser
from hydroponics.settings import BASE_DIR

import logging
log = logging.getLogger('hydro')


class Command(BaseCommand):
	help = 'Opens the Hydro Documentation.'

	def handle(self, *args, **options):
		"""Opens the sphinx documentation.

			:returns: None
			"""
		log.info("Opening docs...")

		url = 'file://' + os.path.join(BASE_DIR, 'sphinx/_build/html/index.html')

		webbrowser.open_new_tab(url)

		log.info("Successfully opened docs.")
