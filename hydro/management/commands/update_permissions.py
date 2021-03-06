from django.core.management.base import BaseCommand
import subprocess

import logging

log = logging.getLogger('hydro')


class Command(BaseCommand):
    help = 'Updates permissions for django and apache.'

    def handle(self, *args, **options):
        """Updates permissions for django and apache.

        :returns: None
        """
        log.info("Updating permissions...")
        commands = ["sudo groupadd super_group",
                    "sudo gpasswd -a www-data super_group",
                    "sudo gpasswd -a pi super_group",
                    "sudo adduser www-data gpio",
                    "sudo adduser pi gpio",
                    "sudo chown :super_group ~/pyprojects/hydroponics/databases",
                    "sudo chown :super_group ~/pyprojects/hydroponics/databases/db.sqlite3",
                    "sudo chmod 664 ~/pyprojects/hydroponics/databases/db.sqlite3",
                    "sudo chown :super_group ~/pyprojects/hydroponics/logs",
                    "sudo chown :super_group ~/pyprojects/hydroponics/logs/db.log",
                    "sudo chown :super_group ~/pyprojects/hydroponics/logs/hydro.log",
                    "sudo chmod 774 ~/pyprojects/hydroponics/logs/db.log",
                    "sudo chmod 774 ~/pyprojects/hydroponics/logs/hydro.log",
                    "sudo chown :super_group /dev",
                    "sudo chown :super_group /dev/i2c-1",
                    "sudo chmod 774 /dev/i2c-1",
                    "sudo chown :super_group ~",
                    "sudo chown :super_group ~/pyprojects/",
                    "sudo chown :super_group ~/pyprojects/hydroponics",
                    "sudo chown :super_group ~/pyprojects/hydroponics/hydroponics",
                    "sudo chown :super_group ~/pyprojects/hydroponics/hydroponics/wsgi.py",
                    "sudo chmod 774 ~/pyprojects/hydroponics/hydroponics/wsgi.py",
                    "sudo chown :super_group ~/pyprojects/hydroponics/testing/selenium_drivers/chromedriver",
                    "sudo chown :super_group ~/pyprojects/hydroponics/testing/selenium_drivers/pidriver",
                    "sudo chown :super_group ~/pyprojects/hydroponics/testing/selenium_drivers/phantomjs",
                    "sudo chmod 774 ~/pyprojects/hydroponics/testing/selenium_drivers/chromedriver",
                    "sudo chmod 774 ~/pyprojects/hydroponics/testing/selenium_drivers/pidriver",
                    "sudo chmod 774 ~/pyprojects/hydroponics/testing/selenium_drivers/phantomjs"]

        for command in commands:
            self.run_command(command)

    def run_command(self, command):
        log.info("Executing shell command: " + command)
        cmd = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        line = cmd.stdout.readline()
        while line:
            log.info("\t" + line.decode('utf-8').rstrip('\n'))
            line = cmd.stdout.readline()
