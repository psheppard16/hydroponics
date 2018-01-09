from django.core.management.base import BaseCommand, CommandError
import subprocess, os
from hydroponics.settings import BASE_DIR

import logging
log = logging.getLogger('hydro')


class Command(BaseCommand):
	help = 'Builds sphinx documentation.'

	def handle(self, *args, **options):
		"""Builds sphinx documentation.

			:returns: None
			"""

		log.info("Building docs...")

		pwd = os.path.join(BASE_DIR, 'sphinx')

		if os.path.isdir(os.path.join(pwd, '_build')):
			# empty the docs build directory
			print(subprocess.Popen("rm -r " + os.path.join(pwd, '_build'), shell=True, stdout=subprocess.PIPE).stdout.read())
		else:
			# create the directory
			os.makedirs(os.path.join(pwd, '_build'))

		# run sphinx make command
		cmd = subprocess.Popen("cd " + pwd + " && make html", shell=True, stdout=subprocess.PIPE)
		while True:
			line = cmd.stdout.readline()
			if not line:
				break

			print(line.rstrip('\n'))
