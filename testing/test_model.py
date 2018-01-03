import time
from django.test import LiveServerTestCase
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import testing.support_methods as sup
from django.core.urlresolvers import reverse
from dateutil.relativedelta import relativedelta
from datetime import datetime

class ModelTestCase(LiveServerTestCase):
	fixtures = ['testing.json']

	def setUp(self):
		"""Set up the selenium driver, and query the necessary entries for tests.

			:returns: None
			"""

		self.driver = sup.get_driver()

	def tearDown(self):
		"""Quit the selenium driver.

			:returns: None
			"""

		self.driver.quit()

	def test_load(self):
		"""Attempt to load

				-assert

			:returns: None
			"""

		print('\n##########################################\n CR: Beginning test_load\n##########################################')