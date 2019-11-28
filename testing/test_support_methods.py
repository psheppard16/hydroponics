import time
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from datetime import datetime
from django.utils.timezone import utc
import testing.support_methods as sup
from django.urls import reverse


class SupportMethodsTestCase(StaticLiveServerTestCase):
    fixtures = ['testing.json']

    def setUp(self):
        """Set up the selenium driver, and query the necessary entries for tests.

            :returns: None
            """
        self.driver = sup.get_driver()

        self.test_path = "/templates/testing/widgets.html"

    def tearDown(self):
        """Quit the selenium driver.

            :returns: None
            """
        self.driver.quit()

    def test_load(self):
        """Attempt to load the test widget page.

                -assert the test file was loaded

            :returns: None
            """

        print(
            '\n##########################################\n Support: Beginning test_load\n##########################################')

        # load the widget test page
        sup.open(self, self.test_path)

        expected = "/templates/testing/widgets.html"
        in_text = self.driver.current_url
        sup.assert_in(expected, in_text, message="Browser did not load Test Page")

    def test_set_chosen_single(self):
        """Attempt to select an option in a single-select.

            - assert every option in the chosen-single is able to be selected

            - assert that attempting to select a value not in the chosen-single raises a ValueError

            :returns: None
            """

        print(
            '\n##########################################\n Support: Beginning test_set_chosen_single\n##########################################')

        # load the widget test page
        sup.open(self, self.test_path)

        # the test chosen-single id
        id = 'id_chosen_single'

        # the options in the test chosen-single element
        options = ["Option 1", "Option 2", "Option 3", "Option 4", "Option 5"]

        for option in options:
            # attempt to set the chosen to the given option
            sup.set_chosen_single(self.driver, id, option)

            # assert that the option has been correctly selected
            chosen = WebDriverWait(self.driver, 3).until(EC.presence_of_element_located(
                (By.XPATH, './/div[@id="' + id + '_chosen"]/a[@class="chosen-single"]/span')))
            sup.assert_equals(option, str(chosen.text), id)

        # attempt to select a value that is not in the test chosen-single
        # assert that a value error is thrown
        self.assertRaises(ValueError, sup.set_chosen_single, self.driver, id, "Option 10000")

    def test_set_chosen_multi(self):
        """Attempt to select an option in a multi-select.

            - assert every option in the chosen-multi is able to be selected

            - assert that multiple values can be selected at once

            - assert that attempting to select a value not in the chosen-multi raises a ValueError

            :returns: None
            """

        print(
            '\n##########################################\n Support: Beginning test_set_chosen_multi\n##########################################')

        # load the widget test page
        sup.open(self, self.test_path)

        # the test chosen-multi id
        id = 'id_chosen_multi'

        # the options in the test chosen-multi element
        options = ["Option 1", "Option 2", "Option 3", "Option 4", "Option 5"]

        for option in options:
            # attempt to set the chosen to the given option
            sup.set_chosen_multi(self.driver, id, [option])

            # assert that the option has been correctly selected
            chosen = WebDriverWait(self.driver, 3).until(EC.presence_of_element_located(
                (By.XPATH,
                 './/div[@id="' + id + '_chosen"]/ul[@class="chosen-choices"]/li[@class="search-choice"]/span')))
            sup.assert_equals(option, str(chosen.text), id)

            # attempt to clear value
            clear = WebDriverWait(self.driver, 3).until(EC.element_to_be_clickable(
                (By.XPATH,
                 './/div[@id="' + id + '_chosen"]/ul[@class="chosen-choices"]/li[@class="search-choice"]/a[@class="search-choice-close"]')))
            clear.click()

        # select all of the options
        for option in options:
            sup.set_chosen_multi(self.driver, id, [option])

        # assert that all of the options have been selected
        for option in options:
            chosen = WebDriverWait(self.driver, 3).until(EC.presence_of_element_located(
                (By.XPATH,
                 './/div[@id="' + id + '_chosen"]/ul[@class="chosen-choices"]/li[@class="search-choice"]/span')))
            sup.assert_equals(option, str(chosen.text), id)

            clear = WebDriverWait(self.driver, 3).until(EC.element_to_be_clickable(
                (By.XPATH,
                 './/div[@id="' + id + '_chosen"]/ul[@class="chosen-choices"]/li[@class="search-choice"]/a[@class="search-choice-close"]')))
            clear.click()

        # attempt to select a value that is not in the test chosen-single
        # assert that a value error is thrown
        self.assertRaises(ValueError, sup.set_chosen_single, self.driver, id, "Option 10000")

    def test_set_date(self):
        """Attempt to set multiple different dates.

            - assert date in datetimepicker is July 4 2100  1:35PM when setting Jul 4 2100  1:36PM'

            - assert date in datetimepicker is Dec 26 1900  12:00AM when setting Dec 25 1900  12:57PM

            - assert date in datetimepicker is within 3 minutes of today's date

            :returns: None
            """

        print(
            '\n##########################################\n Support: Beginning test_set_date\n##########################################')

        # load the widget test page
        sup.open(self, self.test_path)

        # attempt to set far in future date
        far_date = datetime.strptime('Jul 4 2100  1:36PM', '%b %d %Y %I:%M%p')
        sup.set_date(self.driver, 'id_datetime_picker', far_date)

        # check if value of text box matches date
        expected = datetime.strptime('Jul 4 2100  1:36PM', '%b %d %Y %I:%M%p')
        actual = datetime.strptime(sup.get_text(self.driver, 'id_datetime_picker'), '%m/%d/%Y %I:%M %p')
        sup.assert_equals(expected, actual, id='id_datetime_picker')

        time.sleep(1)

        # attempt to set far in past date
        past_date = datetime.strptime('Dec 25 1900  12:00AM', '%b %d %Y %I:%M%p')
        sup.set_date(self.driver, 'id_datetime_picker', past_date)

        # check if value of text box matches date
        expected = datetime.strptime('Dec 25 1900  12:00AM', '%b %d %Y %I:%M%p')
        actual = datetime.strptime(sup.get_text(self.driver, 'id_datetime_picker'), '%m/%d/%Y %I:%M %p')
        sup.assert_equals(expected, actual, id='id_datetime_picker')

        time.sleep(1)

        # attempt to just time
        past_date = datetime.strptime('Dec 25 1900  12:00AM', '%b %d %Y %I:%M%p')
        sup.set_date(self.driver, 'id_time_picker', past_date)

        # check if value of text box matches date
        expected = datetime.strptime('12:00 AM', '%I:%M %p')
        actual = datetime.strptime(sup.get_text(self.driver, 'id_time_picker'), '%I:%M %p')
        sup.assert_equals(expected, actual, id='id_time_picker')

        time.sleep(1)

        # attempt to just date
        past_date = datetime.strptime('Dec 25 1900', '%b %d %Y')
        sup.set_date(self.driver, 'id_date_picker', past_date)

        # check if value of text box matches date
        expected = datetime.strptime('Dec 25 1900', '%b %d %Y')
        actual = datetime.strptime(sup.get_text(self.driver, 'id_date_picker'), '%m/%d/%Y')
        sup.assert_equals(expected, actual, id='id_date_picker')

    def test_round_time(self):
        """Assert that various datetimes with different rounding resolutions are correct.

            - assert 12:07:25 rounded to nearest 60s rounds to 12:07:00

            - assert 12:07:35 rounded to nearest 60s rounds to 12:08:00

            - assert 12:07:25 rounded to nearest 300s rounds to 12:05:00

            - assert 12:07:35 rounded to nearest 300s rounds to 12:10:00

            - assert 12:27:25 rounded to nearest 3600s rounds to 12:00:00

            - assert 12:37:25 rounded to nearest 3600s rounds to 1:00:00

            :returns: None
            """

        print(
            '\n##########################################\n Support: Beginning test_round_time\n##########################################')

        # round down to minute
        date = datetime(2017, 9, 15, hour=12, minute=7, second=25, tzinfo=utc)
        actual = sup.round_time(date, roundTo=60)
        expected = datetime(2017, 9, 15, hour=12, minute=7, tzinfo=utc)
        sup.assert_equals(expected, actual)

        # round up to minute
        date = datetime(2017, 9, 15, hour=12, minute=7, second=35, tzinfo=utc)
        actual = sup.round_time(date, roundTo=60)
        expected = datetime(2017, 9, 15, hour=12, minute=8, tzinfo=utc)
        sup.assert_equals(expected, actual)

        # round down to nearest 5 minutes
        date = datetime(2017, 9, 15, hour=12, minute=7, second=25, tzinfo=utc)
        actual = sup.round_time(date, roundTo=300)
        expected = datetime(2017, 9, 15, hour=12, minute=5, tzinfo=utc)
        sup.assert_equals(expected, actual)

        # round up to nearest 5 minutes
        date = datetime(2017, 9, 15, hour=12, minute=7, second=35, tzinfo=utc)
        actual = sup.round_time(date, roundTo=300)
        expected = datetime(2017, 9, 15, hour=12, minute=10, tzinfo=utc)
        sup.assert_equals(expected, actual)

        # round down to nearest hour
        date = datetime(2017, 9, 15, hour=12, minute=27, second=25, tzinfo=utc)
        actual = sup.round_time(date, roundTo=3600)
        expected = datetime(2017, 9, 15, hour=12, tzinfo=utc)
        sup.assert_equals(expected, actual)

        # round up to nearest hour
        date = datetime(2017, 9, 15, hour=12, minute=37, second=35, tzinfo=utc)
        actual = sup.round_time(date, roundTo=3600)
        expected = datetime(2017, 9, 15, hour=13, tzinfo=utc)
        sup.assert_equals(expected, actual)

    def test_set_text_box(self):
        """Attempt to set the text in a text area, a text field, and a readonly text field.

            - assert setting a text_box to "test" works properly

            - assert setting a text_area to "test" works properly

            - assert setting a readonly test_box to "test" raises an exception

            :returns: None
            """

        print(
            '\n##########################################\n Support: Beginning test_set_text_box\n##########################################')

        # load the widget test page
        sup.open(self, self.test_path)

        # attempt to set the text box to "test"
        id = "id_input"
        sup.set_text_box(self.driver, id, "test")
        expected = "test"
        text_box = WebDriverWait(self.driver, 3).until(EC.presence_of_element_located((By.ID, id)))
        actual = str(text_box.get_attribute("value"))
        sup.assert_equals(expected, actual, id=id)

        # attempt to set the text area to "test"
        id = "id_text_area"
        sup.set_text_box(self.driver, id, "test")
        expected = "test"
        text_area = WebDriverWait(self.driver, 3).until(EC.presence_of_element_located((By.ID, id)))
        actual = str(text_area.get_attribute("value"))
        sup.assert_equals(expected, actual, id=id)

        # attempt to set the read-only text box to "test"
        id = "id_input_readonly"
        self.assertRaises(Exception, sup.set_text_box, self.driver, id, "text")

    def test_get_chosen_single(self):
        """Attempt to get the text from a chosen single at various values

            - assert that get_chosen_single returns the default chosen_single value of "Option 1"

            - assert that get_chosen_single returns the new chosen_single value of "Option 4"

            - assert that get_chosen_single returns the default chosen_single value of ""

            :returns: None
            """

        print(
            '\n##########################################\n Support: Beginning test_get_chosen_single\n##########################################')

        # load the widget test page
        sup.open(self, self.test_path)

        # test that get_chosen_single returns correctly on chosen single with a default value
        id = "id_chosen_single"
        expected = "Option 1"
        actual = sup.get_chosen_single(self.driver, id)
        sup.assert_equals(expected, actual, id=id)

        # test that get_chosen_single returns correctly on chosen single with a new value
        sup.set_chosen_single(self.driver, id, "Option 4")
        expected = "Option 4"
        actual = sup.get_chosen_single(self.driver, id)
        sup.assert_equals(expected, actual, id=id)

        # test that get_chosen_single returns correctly on empty chosen single
        id = "id_chosen_single_empty"
        expected = "Select an Option"
        actual = sup.get_chosen_single(self.driver, id)
        sup.assert_equals(expected, actual, id=id)

    def test_get_chosen_multi(self):
        """Attempt to

            - assert get_chosen_multi returns [] when the multiselect is empty

            - assert get_chosen_multi returns ["Option 1"] when the multiselect has ["Option 1"]

            - assert get_chosen_multi returns ["Option 1", "Option 4"] when the multiselect has ["Option 1", "Option 4"]

            :returns: None
            """

        print(
            '\n##########################################\n Support: test_get_chosen_multi\n##########################################')

        # load the widget test page
        sup.open(self, self.test_path)

        # assert get_chosen_multi returns [] when the multiselect is empty
        id = "id_chosen_multi"
        expected = []
        actual = sup.get_chosen_multi(self.driver, id)
        sup.assert_equals(expected, actual, id=id)

        # add "Option 1" to the chosen multi and assert that get_chosen_multi returns ["Option 1"]
        sup.set_chosen_multi(self.driver, id, ["Option 1"])
        expected = ["Option 1"]
        actual = sup.get_chosen_multi(self.driver, id)
        sup.assert_equals(expected, actual, id=id)

        # add "Option 4" to the chosen multi and assert that get_chosen_multi returns ["Option 1", "Option 4"]
        sup.set_chosen_multi(self.driver, id, ["Option 4"])
        expected = ["Option 1", "Option 4"]
        actual = sup.get_chosen_multi(self.driver, id)
        sup.assert_equals(expected, actual, id=id)

    def test_get_text(self):
        """Attempt to get the text from a text field with various values

            - assert that get_text returns "" when the text_area is empty
            - assert that get_text returns "test" when the text_area has "test"

            - assert that get_text returns "" when the input is empty
            - assert that get_text returns "test" when the input has "test"

            :returns: None
            """

        print(
            '\n##########################################\n Support: Beginning test_get_text\n##########################################')

        # load the widget test page
        sup.open(self, self.test_path)

        # assert returns "" then the text_box is empty
        id = "id_input"
        expected = ""
        actual = sup.get_text(self.driver, id)
        sup.assert_equals(expected, actual, id=id)

        # assert returns "test" then the text_box has "test"
        sup.set_text_box(self.driver, id, "test")
        expected = "test"
        actual = sup.get_text(self.driver, id)
        sup.assert_equals(expected, actual, id=id)

        # assert returns "" then the text_area is empty
        id = "id_text_area"
        expected = ""
        actual = sup.get_text(self.driver, id)
        sup.assert_equals(expected, actual, id=id)

        # assert returns "test" then the text_area has "test"
        sup.set_text_box(self.driver, id, "test")
        expected = "test"
        actual = sup.get_text(self.driver, id)
        sup.assert_equals(expected, actual, id=id)

    def test_element_exists(self):
        """Attempt to check for a real and fake element using css_selector, xpath, and id.

            - assert find element by xpath for "//*[@id='id_input']" returns true

            - assert find element by css_selector for "input#id_input" returns true

            - assert find element by id for "id_input" returns true

            - assert find element by xpath for "//*[@id='id_fake']" returns False

            - assert find element by css_selector for "fake#id_fake" returns False

            - assert find element by id for "id_fake" returns False

            - assert find element with no search options raises a ValueError

            :returns: None
            """

        print(
            '\n##########################################\n Support: Beginning test_element_exists\n##########################################')

        # load the widget test page
        sup.open(self, self.test_path)

        # assert that searching by id, xpath, and css_selector for a real element all return True
        actual = sup.element_exists(self.driver, xpath="//*[@id='id_input']")
        expected = True
        sup.assert_equals(expected, actual)

        actual = sup.element_exists(self.driver, css_selector="input#id_input")
        expected = True
        sup.assert_equals(expected, actual)

        actual = sup.element_exists(self.driver, id="id_input")
        expected = True
        sup.assert_equals(expected, actual)

        # assert that searching by id, xpath, and css_selector for a fake element all return False
        actual = sup.element_exists(self.driver, xpath="//*[@id='id_fake']")
        expected = False
        sup.assert_equals(expected, actual)

        actual = sup.element_exists(self.driver, css_selector="fake#id_fake")
        expected = False
        sup.assert_equals(expected, actual)

        actual = sup.element_exists(self.driver, id="id_fake")
        expected = False
        sup.assert_equals(expected, actual)

        # assert that attempting to search with no search option produces a ValueError
        self.assertRaises(ValueError, sup.element_exists, self.driver)

    def test_open(self):
        """Attempt to open every page in status.

            - assert the home page loads correctly

            - assert the chemical page loads correctly

            - assert the waste page loads correctly

            - assert the control page loads correctly

            :returns: None
            """

        print(
            '\n##########################################\n Support: Beginning test_open\n##########################################')

        pages = ["home", "chemical", "waste", "control"]
        for page in pages:
            # load the home page and assert the url is correct
            sup.open(self, reverse(page))
            expected = reverse(page)
            in_text = self.driver.current_url
            sup.assert_in(expected, in_text, message="Browser did not load %s Page" % page)

    def test_get_all_data(self):
        """Test if get_all_data returns the correct data for the test page

            - assert get_all_data returns the correct data on the default test page

            - assert get_all_data returns the correct data on the test page with modified information

            :returns: None
            """

        print(
            '\n##########################################\n Support: Beginning test_get_all_data \n##########################################')

        # load the widget test page
        sup.open(self, self.test_path)

        # test if the data is correct on the default test page
        actual = sup.get_all_data(self.driver)
        expected = {'id_datetime_picker': '', 'id_time_picker': '', 'id_date_picker': '',
                    'id_chosen_single': 'Option 1', 'id_chosen_single_empty': 'Select an Option',
                    'id_text_area': '', 'id_input': '', 'id_input_readonly': '', 'id_chosen_multi': []}
        sup.assert_equals(expected, actual,
                          message="get_all_data did not fetch the expected values for the default test page")

        # set the values of the elements on the test page
        sup.set_date(self.driver, 'id_datetime_picker', datetime(2017, 9, 5, hour=9, minute=25))
        sup.set_date(self.driver, 'id_time_picker', datetime(2017, 9, 5, hour=9, minute=25))
        sup.set_date(self.driver, 'id_date_picker', datetime(2017, 9, 5, hour=9, minute=25))
        sup.set_chosen_single(self.driver, 'id_chosen_single', 'Option 3')
        sup.set_text_box(self.driver, 'id_text_area', 'Test 1')
        sup.set_text_box(self.driver, 'id_input', 'Test 2')
        sup.set_chosen_multi(self.driver, 'id_chosen_multi', ["Option 3", "Option 1", "Option 2"])

        # test if the data is correct
        actual = sup.get_all_data(self.driver)
        expected = {'id_datetime_picker': '09/05/2017 9:25 AM', 'id_time_picker': '9:25 AM',
                    'id_date_picker': '09/05/2017', 'id_chosen_single': 'Option 3',
                    'id_chosen_single_empty': 'Select an Option', 'id_text_area': 'Test 1', 'id_input': 'Test 2',
                    'id_input_readonly': '', 'id_chosen_multi': ["Option 3", "Option 1", "Option 2"]}
        sup.assert_equals(expected, actual,
                          message="get_all_data did not fetch the expected values for the edited test page")
