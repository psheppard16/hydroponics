import contextlib
import time
from datetime import datetime

import django.db
from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.utils.timezone import utc
from django.utils import timezone
import requests
import textwrap
from hydro.models import *
import string

printable = set(string.printable)
from bs4 import BeautifulSoup

from hydroponics.settings import *


class Command(BaseCommand):
    help = 'Creates a fixture using the database setup commands'

    def add_arguments(self, parser):
        parser.add_argument(
            '--delete',
            dest='delete',
            default=False,
            help='Delete temporary database after creating the fixture',
        )

    def handle(self, *args, **options):
        """Creates a clean database or uses the existing temporary database, populates it with the necessary database
            entries for testing, then uses the populated database to create a fixture, which is stored as
            "hydro/fixtures/testing.json", and then deletes the temporary database if desired.

            :param delete: whether to delete the database after completion
            :returns: None
            """
        db_dict = {'ENGINE': 'django.db.backends.sqlite3',
                   'NAME': os.path.join(BASE_DIR, 'databases/temp.sqlite3')}

        # create or use the existing temporary database
        with create_db(db_dict, usingname='temp', delete=options['delete']) as temp_db:
            call_command("migrate", database=temp_db)
            print("##########################################")
            print("migration successful")
            print("##########################################")

            # generate pseudo-random data by pulling the html from an archived version of Obama's wikipedia page
            data = DataGenerator('https://en.wikipedia.org/wiki/Barack_Obama', datetime(2017, 9, 15, tzinfo=utc))
            print("##########################################")
            print("initialized data generator")
            print("##########################################")

            # populate the database with the necessary testing entries
            create_all(temp_db, data)
            print("##########################################")
            print("object creation successful")
            print("##########################################")

            # create the fixture
            call_command("dumpdata", database=temp_db, output="hydro/fixtures/testing.json",
                         format="json", natural_foreign=True, natural_primary=True, indent=True,
                         exclude=['contenttypes', "sessions", "auth.Permission", "admin"])
            print("##########################################")
            print("fixture creation successful")
            print("##########################################")


# WARNING: There is a race condition based on usingname among threads. You should wrap the using name in a threadlocal or equivalent.
@contextlib.contextmanager
def create_db(db_dict, usingname='_temp_db', delete=False):
    """Creates a database, creates django database connection using its database deifnition, yields its name,
        and finally removes the databse from django's connections and deletes it if desired.

        :param usingname: the name of the temporary fixture creation database
        :param db_dict: the database definition
        :param delete: whether to delete the database after completion
        :returns: None
        """

    insert_db(db_dict, usingname)
    try:
        yield usingname
    finally:
        remove_db(usingname, delete=delete)


def insert_db(definition, using):
    """Creates a django database connection for the given database

        :param using: the temporary fixture creation database
        :param definition: the database definition
        :returns: using
        """

    if using in django.db.connections.databases:
        raise ValueError('%s already exists' % using)
    if using in django.db.connections:
        raise ValueError('%s already exists' % using)
    django.db.connections.databases[using] = definition
    return using


def remove_db(using, delete=False):
    """Deletes the database if delete=True and it exists, otherwise clost the django database connection.

        :param using: the temporary fixture creation database
        :param delete: whether to delete the database
        :returns: None
        """

    if delete and os.path.isfile(django.db.connections.databases[using]['NAME']):
        os.remove(django.db.connections.databases[using]['NAME'])
    del django.db.connections.databases[using]
    try:
        conn = django.db.connections[using]
        conn.close()
    except Exception:
        pass
    try:
        delattr(django.db.connections._connections, using)
    except Exception:
        pass
    assert not hasattr(django.db.connections._connections, using), "Could not remove database wrapper %s" % (using)


def create_all(database, data):
    waste, created = ChemicalSettings.objects.db_manager(database).update_or_create(id=1,
                                                                                    defaults={
                                                                                        "auto_regulate_pH": "False",
                                                                                        "low_pH": "5",
                                                                                        "high_pH": "7",
                                                                                        "pH_adj_volume": "1",
                                                                                        "last_pH_change": timezone.now(),
                                                                                        "auto_regulate_nutrients": "False",
                                                                                        "low_EC": "5",
                                                                                        "high_EC": "7",
                                                                                        "nutrient_adj_volume": "1",
                                                                                        "last_nutrient_change": timezone.now(),
                                                                                        "auto_regulate_ORP": "False",
                                                                                        "low_ORP": "5",
                                                                                        "high_ORP": "7",
                                                                                        "ORP_adj_volume": "1",
                                                                                        "last_ORP_change": timezone.now(),
                                                                                        "min_change_interval": "2",
                                                                                        "polling_range": "1",
                                                                                        "minimun_data_count": "60"})

    chemical, created = WasteSettings.objects.db_manager(database).update_or_create(id=1,
                                                                                    defaults={
                                                                                        "auto_water_change": "False",
                                                                                        "last_water_change": timezone.now(),
                                                                                        "maximum_water_change_interval": "30",
                                                                                        "minimum_water_change_interval": "1",
                                                                                        "auto_pump": "False",
                                                                                        "auto_refill": "False",
                                                                                        "resevoir_volume": "90",
                                                                                        "basin_volume": "90"})

    pH, created = DataType.objects.db_manager(database).update_or_create(id=1, defaults={"type": "pH"})
    EC, created = DataType.objects.db_manager(database).update_or_create(id=2, defaults={"type": "EC"})
    ORP, created = DataType.objects.db_manager(database).update_or_create(id=3, defaults={"type": "ORP"})

    requested, created = Status.objects.db_manager(database).update_or_create(id=1, defaults={"status": "requested"})
    completed, created = Status.objects.db_manager(database).update_or_create(id=2, defaults={"status": "completed"})
    canceled, created = Status.objects.db_manager(database).update_or_create(id=3, defaults={"status": "canceled"})
    failed, created = Status.objects.db_manager(database).update_or_create(id=4, defaults={"status": "failed"})

    increase_pH, created = RequestType.objects.db_manager(database).update_or_create(id=1,
                                                                                     defaults={"type": "increase_pH"})
    decrease_pH, created = RequestType.objects.db_manager(database).update_or_create(id=2,
                                                                                     defaults={"type": "decrease_pH"})
    increase_nutrients, created = RequestType.objects.db_manager(database).update_or_create(id=3, defaults={
        "type": "increase_nutrients"})
    refill, created = RequestType.objects.db_manager(database).update_or_create(id=4, defaults={"type": "refill"})
    water_change, created = RequestType.objects.db_manager(database).update_or_create(id=5,
                                                                                      defaults={"type": "water_change"})
    start_pump, created = RequestType.objects.db_manager(database).update_or_create(id=6,
                                                                                    defaults={"type": "start_pump"})
    stop_pump, created = RequestType.objects.db_manager(database).update_or_create(id=7, defaults={"type": "stop_pump"})


def str_time_prop(start, end, format, prop):
    """Get the time that is some fraction between two other times.

        :param start: a Datetime object giving the start of the interval
        :param start: a Datetime object giving the end of the interval
        :param format: the datetime format of start and end
        :param prop: what proportion of the interval after the start time the desired date is
        :returns: Datetime: a Datetime in the desired format
        """

    stime = time.mktime(time.strptime(start, format))
    etime = time.mktime(time.strptime(end, format))

    ptime = stime + prop * (etime - stime)

    return time.strftime("%Y-%m-%d %H:%M:%S%z", time.localtime(ptime))


def generate_date(start, end, prop):
    """A wrapper for str_time_prop which uses dates in the format '%m/%d/%Y %I:%M %p'.

        :param start: a Datetime object giving the start of the interval
        :param start: a Datetime object giving the end of the interval
        :param prop: what proportion of the interval after the start time the desired date is
        :returns: Datetime: a Datetime in the desired format
        """
    return str_time_prop(start, end, '%m/%d/%Y %I:%M %p', prop)


class DataGenerator:
    """Fetches the html form an archived site at a given date, and then parses it.

        :param url: the url of the archived site
        :param date: the date of the archived site

        :returns: None
        """

    def __init__(self, url, date):
        self.url = url
        self.date = date

        self.__parse()

    def __parse(self):
        """Get website from archive.org and parse it with Beautiful Soup.

            """
        # build archive.org url
        request_url = 'https://web.archive.org/web/' + self.date.strftime('%Y%m%d%H%M%S') + '/' + self.url

        # create request
        r = requests.get(request_url)
        if r.status_code != 200:
            raise Exception('Request to URL failed. HTTP Status: ' + str(r.status_code))

        # parse site
        self.parsed_html = BeautifulSoup(r.text, 'lxml')

    def partition(self, length=100, tags=None):
        """Split site text into equal parts.

            :param length: the length to split the text by
            :param tags: the html tags to harvest text from

            :returns: tuple
            """

        if tags is None:
            tags = ['p']

        text_str = ''
        for tag in tags:
            # find all elements with tag
            elements = self.parsed_html.find_all(tag)

            # combine text from all elements
            for element in elements:
                text_str += element.get_text()

        text_str = filter(lambda x: x in printable, text_str)
        strs = textwrap.wrap(text_str, length)

        if len(strs[-1]) != 100:
            strs.pop(-1)

        return strs
