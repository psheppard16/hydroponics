from django.core.management.base import BaseCommand, CommandError
import subprocess, os
from hydroponics.settings import BASE_DIR
from shutil import copyfile

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
            self.run_command("rm -r " + os.path.join(pwd, '_build'))
        else:
            # create the directory
            os.makedirs(os.path.join(pwd, '_build'))

        # run sphinx make command
        self.run_command("cd " + pwd + " && make html")

    def run_command(self, command):
        log.info("Executing shell command: " + command)
        cmd = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        line = cmd.stdout.readline()
        while line:
            log.info("\t" + line.decode('utf-8').rstrip('\n'))
            line = cmd.stdout.readline()
