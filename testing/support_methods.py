import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementNotVisibleException, TimeoutException
from sys import platform
from selenium import webdriver
from hydroponics.settings import BASE_DIR
import datetime as dt
import os


def set_chosen_single(driver, id, value):
	"""Gets the chosen single-select element of the passed id and attempts to
		select the passed value.

		:param driver: The driver used to find the html element
		:param id: The id of the chosen single-select
		:param value: The text value to select from the chosen select
		:raises: ValueError: Could not find the value in the chosen single-select
		:raises: TimeoutException: Could not find an element of the passed id
		:returns: None
		"""
	id += "_chosen"

	#find the chosen single-select and its parent and wait until they are clickable
	chosen = WebDriverWait(driver, 3).until(
		EC.element_to_be_clickable((By.ID, id)))
	parent = WebDriverWait(chosen, 3).until(
		EC.element_to_be_clickable((By.XPATH, '../..')))

	#click parent to remove inconsistencies involving parent divs containing multiple elements
	parent.click()
	chosen.click()

	# sleep to allow time for ?something?
	time.sleep(.1)

	# find the textbox inside the single-select and wait until it is clickable
	text = WebDriverWait(chosen, 3).until(EC.presence_of_element_located(
		(By.XPATH, './/input[@type="text"][@autocomplete="off"]')))

	# enter value into the textbox and wait until the value is present
	text.send_keys(value)
	WebDriverWait(chosen, 3).until(EC.text_to_be_present_in_element_value(
		(By.XPATH, './/input[@type="text"][@autocomplete="off"]'), value))

	# get the results from entering the value into the textbox
	results = WebDriverWait(chosen, 3).until(
		EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".chosen-results li")))

	# check to see if there is an exact match in results and click it
	values = []
	for result in results:
		values.append(result.text)
		if result.text == value:
			result.click()
			WebDriverWait(driver, 3).until(EC.text_to_be_present_in_element(
				(By.XPATH, './/div[@id="' + id + '"]/a[@class="chosen-single"]/span'), value))
			return
	raise ValueError("Could not find value: '" + str(value) + "' for chosen-single-select: '" + id + "'. Values availible: " + ', '.join(values))


def set_chosen_multi(driver, id, values):
	"""Gets the chosen mutli select element of the passed id and attempts to
		select the passed values.

		:param driver: The driver used to find the html element
		:param id: The id of the chosen mutli select
		:param values: The text values to select from the chosen mutli select
		:raises: ValueError: Could not find the value in the chosen mutli select
		:raises: TimeoutException: Could not find an element of the passed id
		:returns: None
		"""
	id += "_chosen"

	#find the chosen-multi-select and wait until it is clickable
	chosen = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.ID, id)))

	# click parent to remove inconsistencies involving parent divs containing multiple elements
	parent = WebDriverWait(chosen, 3).until(EC.element_to_be_clickable((By.XPATH, '../..')))
	parent.click()

	# click the chosen-multi
	chosen.click()

	# find the textbox inside the chosen multiselect and wait until it is clickable
	text = WebDriverWait(chosen, 3).until(
		EC.element_to_be_clickable((By.XPATH, './/input[@type="text"][@autocomplete="off"]')))
		# .// to limit search to sub-elements

	for value in values:
		text.clear()

		# enter value into the textbox and wait until the value is present
		text.send_keys(value)
		WebDriverWait(chosen, 3).until(EC.text_to_be_present_in_element_value(
			(By.XPATH, './/input[@type="text"][@autocomplete="off"]'), value))

		#get the results from entering the value into the textbox
		results = WebDriverWait(chosen, 3).until(
			EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".chosen-results li")))

		# check to see if there is an exact match in results and click it
		found = False
		values = []
		for result in results:
			values.append(result.text)
			if result.text == value:
				result.click()
				found = True
				break
		if not found:
			raise ValueError("Could not find value: '" + str(value) + "' for chosen-multi-select: '" + id + "'. Values availible: " + ' '.join(values))


def set_date(driver, id, date):
	"""Sets datetimepicker with given id to given date. Since the datetimepicker only takes times at 5 minute intervals,
		this function automatically rounds the date. 1:36PM and 1:37PM would round to 1:35PM and 1:38PM and 1:39PM would
		round to 1:40PM. Situations when the rounding changes the date are handled and tested.

		:param driver: The driver used to find the html element
		:param id: The id of the datepicker
		:param date: The datetime.datetime object to be picked
		:raises: ValueError: Any part of date is out of range
		:returns: None
		"""
	# find date-picker and wait until it is clickable, and click it
	date_picker_text = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.ID, id)))

	# determine action
	text_classes = date_picker_text.get_attribute("class").split()
	if 'type-time' in text_classes:
		action = 'time'
	elif 'type-date' in text_classes:
		action = 'date'
	else:
		action = 'datetime'

	# click parent to remove inconsistencies involving parent divs containing multiple elements
	if "phantom" in driver.capabilities['browserName'].lower():
		parent = WebDriverWait(date_picker_text, 3).until(EC.element_to_be_clickable((By.XPATH, '../..')))
		parent.click()

	# open date picker by clicking text box
	date_picker_text.click()

	# find datetimepicker div
	date_picker = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.bootstrap-datetimepicker-widget')))

	# scroll into view of date picker
	driver.execute_script("window.scroll(" + str(date_picker_text.location['x']) + "," + str(
		int(date_picker_text.location['y']) + 200) + ");")

	if 'time' in action:
		# open date picker
		if 'date' in action:
			time_picker_parent = WebDriverWait(date_picker, 3).until(
				EC.presence_of_element_located((By.CSS_SELECTOR, 'li.collapse div.timepicker'))).find_element_by_xpath('./..')
			if "show" not in time_picker_parent.get_attribute("class"):
				accordion_toggle = WebDriverWait(date_picker, 3).until(
					EC.element_to_be_clickable((By.CSS_SELECTOR, 'li.accordion-toggle table tbody tr td a')))
				accordion_toggle.click()

		# navigate to minute
		minute = WebDriverWait(date_picker, 3).until(
			EC.element_to_be_clickable(
				(By.CSS_SELECTOR, 'div.timepicker-picker table tr td span.timepicker-minute')))
		while date.minute != int(minute.get_attribute('innerHTML')):

			if int(minute.get_attribute('innerHTML')) < date.minute:
				try:
					inc_btn = WebDriverWait(date_picker, 3).until(
						EC.element_to_be_clickable((By.CSS_SELECTOR,
						                            'div.timepicker-picker table tr td a[data-action="incrementMinutes"]')))

					if 'hidden' in inc_btn.get_attribute('style'):
						raise ValueError(
							"Rounded date: " + date.strftime(
								'%Y-%m-%d %H:%M') + " from: " + date.strftime(
								'%Y-%m-%d %H:%M') + " has year out of valid range.")
					else:
						inc_btn.click()

				except TimeoutException:
					raise ValueError(
						"Rounded date: " + date.strftime('%Y-%m-%d %H:%M') + " from: " + date.strftime(
							'%Y-%m-%d %H:%M') + " has year out of valid range.")

			elif int(minute.get_attribute('innerHTML')) > date.minute:
				try:
					dec_btn = WebDriverWait(date_picker, 3).until(
						EC.element_to_be_clickable((By.CSS_SELECTOR,
						                            'div.timepicker-picker table tr td a[data-action="decrementMinutes"]')))

					if 'hidden' in dec_btn.get_attribute('style'):
						raise ValueError(
							"Rounded date: " + date.strftime(
								'%Y-%m-%d %H:%M') + " from: " + date.strftime(
								'%Y-%m-%d %H:%M') + " has year out of valid range.")
					else:
						dec_btn.click()

				except TimeoutException:
					raise ValueError(
						"Rounded date: " + date.strftime('%Y-%m-%d %H:%M') + " from: " + date.strftime(
							'%Y-%m-%d %H:%M') + " has year out of valid range.")

		# navigate to minute
		hour = WebDriverWait(date_picker, 3).until(
			EC.element_to_be_clickable(
				(By.CSS_SELECTOR, 'div.timepicker-picker table tr td span.timepicker-hour')))
		while int(date.strftime("%I")) != int(hour.get_attribute('innerHTML')):

			if int(hour.get_attribute('innerHTML')) < int(date.strftime("%I")):
				try:
					inc_btn = WebDriverWait(date_picker, 3).until(
						EC.element_to_be_clickable((By.CSS_SELECTOR,
						                            'div.timepicker-picker table tr td a[data-action="incrementHours"]')))

					if 'hidden' in inc_btn.get_attribute('style'):
						raise ValueError(
							"Rounded date: " + date.strftime('%Y-%m-%d %H:%M') + " from: " + date.strftime(
								'%Y-%m-%d %H:%M') + " has year out of valid range.")
					else:
						inc_btn.click()

				except TimeoutException:
					raise ValueError(
						"Rounded date: " + date.strftime('%Y-%m-%d %H:%M') + " from: " + date.strftime(
							'%Y-%m-%d %H:%M') + " has year out of valid range.")

			elif int(hour.get_attribute('innerHTML')) > int(date.strftime("%I")):
				try:
					dec_btn = WebDriverWait(date_picker, 3).until(
						EC.element_to_be_clickable((By.CSS_SELECTOR,
						                            'div.timepicker-picker table tr td a[data-action="decrementHours"]')))

					if 'hidden' in dec_btn.get_attribute('style'):
						raise ValueError(
							"Rounded date: " + date.strftime('%Y-%m-%d %H:%M') + " from: " + date.strftime(
								'%Y-%m-%d %H:%M') + " has year out of valid range.")
					else:
						dec_btn.click()

				except TimeoutException:
					raise ValueError(
						"Rounded date: " + date.strftime('%Y-%m-%d %H:%M') + " from: " + date.strftime(
							'%Y-%m-%d %H:%M') + " has year out of valid range.")

		# change AM/PM
		ampm_btn = WebDriverWait(date_picker, 3).until(
			EC.element_to_be_clickable((By.CSS_SELECTOR,
			                            'div.timepicker-picker table tr td button[data-action="togglePeriod"]')))
		if date.strftime("%p") != ampm_btn.get_attribute('innerHTML'):
			ampm_btn.click()

	if 'date' in action:
		# open date picker
		if 'time' in action:
			date_picker_parent = WebDriverWait(date_picker, 3).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'li.collapse div.datepicker'))).find_element_by_xpath('..')
			if "show" not in date_picker_parent.get_attribute("class"):
				accordion_toggle = WebDriverWait(date_picker, 3).until(
					EC.element_to_be_clickable((By.CSS_SELECTOR, 'li.accordion-toggle table tbody tr td a')))
				accordion_toggle.click()

		# click switch button to display months
		switch = WebDriverWait(date_picker, 3).until(
			EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.datepicker-days table thead tr th.picker-switch')))
		switch.click()

		# update switch reference
		switch = WebDriverWait(date_picker, 3).until(
			EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.datepicker-months table thead tr th.picker-switch')))

		# attempt to navigate to correct year
		while date.year != int(switch.get_attribute('innerHTML')):

			if date.year < int(switch.get_attribute('innerHTML')):
				try:
					prev_btn = WebDriverWait(date_picker, 3).until(
						EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.datepicker-months table thead tr th.prev')))

					if 'hidden' in prev_btn.get_attribute('style'):
						raise ValueError(
							"Rounded date: " + date.strftime('%Y-%m-%d %H:%M') + " from: " + date.strftime(
								'%Y-%m-%d %H:%M') + " has year out of valid range.")
					else:
						prev_btn.click()

				except TimeoutException:
					raise ValueError("Rounded date: " + date.strftime('%Y-%m-%d %H:%M') + " from: " + date.strftime(
						'%Y-%m-%d %H:%M') + " has year out of valid range.")

			elif date.year > int(switch.get_attribute('innerHTML')):
				try:
					next_btn = WebDriverWait(date_picker, 3).until(
						EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.datepicker-months table thead tr th.next')))

					if 'hidden' in next_btn.get_attribute('style'):
						raise ValueError(
							"Rounded date: " + date.strftime('%Y-%m-%d %H:%M') + " from: " + date.strftime(
								'%Y-%m-%d %H:%M') + " has year out of valid range.")
					else:
						next_btn.click()

				except TimeoutException:
					raise ValueError("Rounded date: " + date.strftime('%Y-%m-%d %H:%M') + " from: " + date.strftime(
						'%Y-%m-%d %H:%M') + " has year out of valid range.")

		# click month
		months = WebDriverWait(date_picker, 3).until(
			EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.datepicker-months table tbody tr td span.month')))
		for month in months:
			if month.get_attribute('innerHTML') == date.strftime('%b'):
				if 'disabled' in month.get_attribute('class'):
					raise ValueError("Rounded date: " + date.strftime('%Y-%m-%d %H:%M') + " from: " + date.strftime('%Y-%m-%d %H:%M') + " has month out of valid range.")
				else:
					month.click()
					break

		# click day
		days = WebDriverWait(date_picker, 3).until(
			EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.datepicker-days table tbody tr td.day')))
		for day in days:
			if int(day.get_attribute('innerHTML')) == date.day and 'old' not in day.get_attribute('class') and 'new' not in day.get_attribute('class'):
				if 'disabled' in day.get_attribute('class'):
					raise ValueError("Rounded date: " + date.strftime('%Y-%m-%d %H:%M') + " from: " + date.strftime('%Y-%m-%d %H:%M') + " has day out of valid range.")
				else:
					day.click()
					break

	# close datepicker
	date_picker_text.click()


def round_time(date_time, roundTo=60):
	"""Round a datetime object to any time laps in seconds

		:param date_time: datetime.datetime object, default now.
		:param roundTo: Closest number of seconds to round to, default 1 minute.
		:returns: datetime
	"""
	seconds = (date_time.replace(tzinfo=None) - date_time.min).seconds
	rounding = (seconds + roundTo / 2) // roundTo * roundTo
	return date_time + dt.timedelta(0, rounding - seconds, -date_time.microsecond)


def scroll_to_middle(driver, element):
	scroll_element_into_middle = "var viewPortHeight = Math.max(document.documentElement.clientHeight, window.innerHeight || 0); var elementTop = arguments[0].getBoundingClientRect().top; window.scrollBy(0, elementTop-(viewPortHeight/2));"
	driver.execute_script(scroll_element_into_middle, element)
	time.sleep(0.5)


def set_text_box(driver, id, value):
	"""Gets the text element, clears it,  and enters the passed value.

		:param driver: The driver used to find the html element
		:param id: The id of the text element
		:param value: the string to enter into the text box
		:raises: TimeoutException: Could not find an element of the passed id
		:returns: None
		"""
	text_box = WebDriverWait(driver, 3).until(
		EC.element_to_be_clickable((By.ID, id)))

	if not text_box.get_attribute("readonly"):
		text_box.clear()
		if value:
			text_box.send_keys(value)
			WebDriverWait(driver, 3).until(EC.text_to_be_present_in_element_value((By.ID, id), value))
	else:
		raise Exception("The text box must not be readonly")


def get_chosen_single(driver, id):
	"""Gets the selected value from the chosen single element of the passed id.

		:param driver: The driver used to find the html element
		:param id: The id of the chosen single-select
		:raises: TimeoutException: Could not find an element of the passed id
		:returns: String: the selected value in the chosen single
		"""
	id += "_chosen"
	# Get the selected text from chosen single after waiting for it to be present in the DOM
	chosen = WebDriverWait(driver, 3).until(EC.presence_of_element_located(
		(By.CSS_SELECTOR, 'div#' + str(id) + ".chosen-container.chosen-container-single")))
	return str(chosen.text)


def get_chosen_multi(driver, id):
	"""Gets the selected values from the chosen multi-select element of the passed id.

		:param driver: The driver used to find the html element
		:param id: The id of the chosen mutli select
		:raises: TimeoutException: Could not find an element of the passed id
		:returns: String[]: the list of selected values in the chosen multi
		"""
	id += "_chosen"
	chosen = WebDriverWait(driver,3).until(EC.element_to_be_clickable((By.XPATH, './/div[@id="'+id+'"]/ul[@class="chosen-choices"]')))
	chosens = chosen.find_elements_by_tag_name("li")
	selected_choices = []
	for choice in chosens:
		selected_choices.append(str(choice.text))
	return list(filter(None, selected_choices))


def get_text(driver, id):
	"""Gets the text from the text element of the passed id.

		:param driver: The driver used to find the html element
		:param id: The id of the text element
		:returns: String: the text in the text element
		:raises: TimeoutException: Could not find an element of the passed id
		"""
	text_box = WebDriverWait(driver, 3).until(
		EC.presence_of_element_located((By.ID,id)))
	return str(text_box.get_attribute("value"))


def click_element(driver, id):
	"""Gets the element of the passed id and clicks with it focused.

		:param driver: The driver used to find the html element
		:param id: The id of the element
		:raises: TimeoutException: Could not find an element of the passed id
		"""
	WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.ID, id))).click()


def get_all_data(driver):
	"""Gets all the text from single-selects, inputs, and textareas.

			Todo: add support for multi-selects

		:param driver: The driver used to find the html element
		:param id: The id of the element
		:returns: None
		"""
	data = {}
	elements = WebDriverWait(driver, 3).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '[id]')))
	for element in elements:
		if element.is_displayed():
			type = str(element.tag_name)
			id = str(element.get_attribute('id'))
			if type == "select" or type == "input" or type == "textarea":
				data[id] = get_text(driver, id)
			elif "chosen-container-single" in element.get_attribute("class"):
				data[id[:-7]] = get_chosen_single(driver, id[:-7])  #[:-7] to remove "_chosen" from the ids
			elif "chosen-container-multi" in element.get_attribute("class"):
				data[id[:-7]] = get_chosen_multi(driver, id[:-7])
	return data


def element_exists(driver, xpath=None, css_selector=None, id=None):
	"""Checks if an element exists.

		:param driver: The driver used to find the html element
		:param xpath: a search value for xpath, css_selector, or id
		:param css_selector: a search value for ecss_selector, or id
		:param id: a search value for id
		:returns: bool: whether the element could by found
		:raises: ValueError: Invalid search option
		"""
	if xpath:
		return len(driver.find_elements_by_xpath(xpath)) > 0
	elif css_selector:
		return len(driver.find_elements_by_css_selector(css_selector)) > 0
	elif id:
		return len(driver.find_elements_by_id(id)) > 0
	else:
		raise ValueError("A search option must be provided. One of: xpath, css_selector, or id is required")


def get_driver():
	"""Gets the appropriate selenium driver based on OS, or the
		the driver specified in the environment variable 'driver'.

		:returns: The appropriate selenium driver
		"""
	# determine driver based on OS
	driver_environment_variable = os.environ.get('driver')
	if driver_environment_variable:
		if 'phantomjs' in driver_environment_variable:
			return webdriver.PhantomJS(executable_path=BASE_DIR + '/testing/selenium_drivers/phantomjs')
		elif 'chrome-headless' in driver_environment_variable:
			if platform == "linux" or platform == "linux2":
				chrome_options = webdriver.ChromeOptions()
				chrome_options.add_argument("headless")
				chrome_options.add_argument("disable-extensions")
				chrome_options.add_argument("disable-gpu")
				return webdriver.Chrome(chrome_options=chrome_options, executable_path=BASE_DIR + '/testing/selenium_drivers/chromedriver-linux64')
			else:
				raise Exception("Headless Chrome testing is currently only supported on linux.")
		elif 'chrome' in driver_environment_variable:
			return webdriver.Chrome(executable_path=BASE_DIR + '/testing/selenium_drivers/chromedriver')
		elif 'safari' in driver_environment_variable:
			return webdriver.Safari()
		else:
			raise Exception("Expected: %r, %r, %r, or %r. Was: %r" % ('phantomjs', 'chrome', 'chrome-headless', 'safari', driver_environment_variable))
	else:
		if "darwin" in platform:
			return webdriver.Chrome(executable_path=BASE_DIR + '/testing/selenium_drivers/chromedriver')
		else:
			return webdriver.PhantomJS()


def open(client, url):
	"""Loads the passed url.

		:returns: None
		"""
	client.driver.get(client.live_server_url + url)


def assert_in(expected, in_iter, id=None, message=""):
	"""Asserts that the expected value is in the iterable in_ter, and displays an output message on failure.

		:param expected: The value expected in in_iter
		:param in_iter: The iterable in which the value is expected
		:param id: The optional id of the related html element
		:param message: An optional message to output
		:returns: None
		"""
	if id:
		assert expected in in_iter, message + " Expected: %r In: %r For ID %r" % (expected, in_iter, id)
	else:
		assert expected in in_iter, message + " Expected: %r In: %r" % (expected, in_iter)


def assert_not_in(expected, in_iter, id=None, message=""):
	"""Asserts that the expected value is not in the iterable in_iter, and displays an output message on failure.

		:param expected: The text expected to not be in in_iter
		:param in_iter: The iterable that should not include expected
		:param id: The optional id of the related html element
		:param message: An optional message to output
		:returns: None
		"""
	if id:
		assert expected not in in_iter, message + " Expected: %r Not In: %r For ID %r" % (expected, in_iter, id)
	else:
		assert expected not in in_iter, message + " Expected: %r Not In: %r" % (expected, in_iter)


def assert_equals(expected, actual, id=None, message=""):
	"""Asserts that the expected value equals the actual value, and displays an output message on failure.

		:param expected: The expected value
		:param actual: The actual value
		:param id: The optional id of the related html element
		:param message: An optional message to output
		:returns: None
		"""
	if id:
		assert expected == actual, message + " Expected: %r Was: %r For ID %r" % (expected, actual, id)
	else:
		assert expected == actual, message + " Expected: %r Was: %r" % (expected, actual)


def assert_not_equals(excluded, actual, id=None, message=""):
	"""Asserts that the excluded value does not equal the actual value, and displays an output message on failure.

		:param excluded: The excluded value
		:param actual: The actual value
		:param id: The optional id of the related html element
		:param message: An optional message to output
		:returns: None
		"""
	if id:
		assert excluded != actual, message + " Excluded: %r Was: %r For ID %r" % (excluded, actual, id)
	else:
		assert excluded != actual, message + " Excluded: %r Was: %r" % (excluded, actual)


def assert_not_empty(text, id=None, message=""):
	"""Asserts that the text is not empty quotes, and displays an output message on failure.

		:param text: The text to test
		:param id: The optional id of the related html element
		:param message: An optional message to output
		:returns: None
		"""
	if id:
		assert text != "", message + " Expected: %r Was: %r For ID %r" % ("a value", "empty quotes", id)
	else:
		assert text != "", message + " Expected: %r Was: %r" % ("a value", "empty quotes")


def assert_empty(text, id=None, message=""):
	"""Asserts that the text empty quotes, and displays an output message on failure.

		:param text: The text to test
		:param id: The optional id of the related html element
		:param message: An optional message to output
		:returns: None
		"""
	if id:
		assert text == "", message + " Expected: %r Was: %r For ID %r" % ("empty quotes", text, id)
	else:
		assert text == "", message + " Expected: %r Was: %r" % ("empty quotes", text)

def assert_exists(client, id, exists=True):
	"""Asserts that the html element of the given id exists

		:param id: The id of the html element
		:param message: An optional message to output
		:returns: None
		"""
	if exists:
		try:
			WebDriverWait(client.driver, 3).until(EC.visibility_of_element_located((By.ID, id)))
		except Exception as e:
			assert False, "Element: %r could not be found. Encountered exception: %r" % (id, e)
	else:
		try:
			WebDriverWait(client.driver, 1).until(EC.visibility_of_element_located((By.ID, id)))
		except (TimeoutException, ElementNotVisibleException, NoSuchElementException):
			pass
		except Exception as e:
			assert False, "Exception %r occured while searching for Element %r. Expected one of: TimeoutException, ElementNotVisibleException, NoSuchElementException" % (e, id)

def assert_visible(client, id, visible=True):
	"""Asserts that the html element of the given id is visible

		:param id: The id of the html element
		:param message: An optional message to output
		:returns: None
		"""
	if visible:
		try:
			element = WebDriverWait(client.driver, 3).until(EC.visibility_of_element_located((By.ID, id)))
			assert element.is_displayed(), " Element: %r Was found, but is not displayed" % id
		except Exception as e:
			assert False, "Element: %r could not be found. Encountered exception: %r" % (id, e)
	else:
		try:
			element = WebDriverWait(client.driver, 1).until(EC.visibility_of_element_located((By.ID, id)))
			assert not element.is_displayed(), " Element: %r Was found and is displayed as: %r" % (id, element)
		except (TimeoutException, ElementNotVisibleException, NoSuchElementException):
			pass
		except Exception as e:
			assert False, "Exception %r occured while searching for Element %r. Expected one of: TimeoutException, ElementNotVisibleException, NoSuchElementException" % (e, id)

