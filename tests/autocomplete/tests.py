import json
import time
from django.contrib.admin.views.main import TO_FIELD_VAR
from django.utils.encoding import force_str
from django.test import TestCase, LiveServerTestCase
from django.test import override_settings
from django.test.client import Client
from . import models
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from django import VERSION
LIVE_SERVER_CLASS = LiveServerTestCase
if VERSION >= (1, 7):
    from django.contrib.staticfiles.testing import StaticLiveServerTestCase
    LIVE_SERVER_CLASS = StaticLiveServerTestCase


@override_settings(ROOT_URLCONF="autocomplete.urls")
class AutocompleteTest(TestCase):
    fixtures = ["autocomplete/initial.json"]

    def setUp(self):
        super(AutocompleteTest, self).setUp()
        self.client = Client()

    def test_search(self):
        response = self.client.get("/yaaac/autocomplete/band/search/?%s=id&query=ge&search_fields=^name&suggest_by=name" % TO_FIELD_VAR)
        self.assertEqual(json.loads(force_str(response.content)),
                         {u'query': u'ge', u'suggestions': [{u'data': 1, u'value': u'Genesis'}]})

        response = self.client.get("/yaaac/autocomplete/band/search/?%s=id&query=ge&search_fields=name&suggest_by=get_full_info" % TO_FIELD_VAR)
        self.assertEqual(json.loads(force_str(response.content)),
                         {u'query': u'ge', u'suggestions': [
                             {u'data': 1, u'value': u'Genesis (Rock)'},
                             {u'data': 6, u'value': u'The Bee Gees (Cheese)'},
                         ]})

        response = self.client.get(
            "/yaaac/autocomplete/bandmember/search/?%s=id&query=ph&search_fields=first_name&suggest_by=get_full_name" % TO_FIELD_VAR)
        self.assertEqual(json.loads(force_str(response.content)),
                         {u'query': u'ph', u'suggestions': [
                             {u'data': 1, u'value': u'Phil Collins'},
                             {u'data': 4, u'value': u'Phil Spector'},
                         ]})

        response = self.client.get(
            "/yaaac/autocomplete/bandmember/search/?%s=id&query=ph&search_fields=first_name,last_name&suggest_by=get_full_name" % TO_FIELD_VAR)
        self.assertEqual(json.loads(force_str(response.content)),
                         {u'query': u'ph', u'suggestions': [
                             {u'data': 1, u'value': u'Phil Collins'},
                             {u'data': 4, u'value': u'Phil Spector'},
                         ]})

        response = self.client.get(
            "/yaaac/autocomplete/bandmember/search/?%s=id&query=ph col&search_fields=first_name,last_name&suggest_by=get_full_name" % TO_FIELD_VAR)
        self.assertEqual(json.loads(force_str(response.content)),
                         {u'query': u'ph col', u'suggestions': [
                             {u'data': 1, u'value': u'Phil Collins'},
                         ]})

    def test_search_with_pk(self):
        response = self.client.get("/yaaac/autocomplete/band/search/?pk=1")
        self.assertEqual(json.loads(force_str(response.content)), {'value': 'Genesis', 'url': None})

    def test_search_not_found(self):
        response = self.client.get("/yaaac/auth/user/search/?%s=id&query=super&search_fields=^username&suggest_by=password" % TO_FIELD_VAR)
        self.assertEqual(response.status_code, 404)
        response = self.client.get("/yaaac/auth/user/search/?pk=1")
        self.assertEqual(response.status_code, 404)

    def test_search_not_allowed(self):
        response = self.client.get("/yaaac/autocomplete/instrument/search/?%s=id&query=gui&search_fields=^name&suggest_by=__unicode__" % TO_FIELD_VAR)
        self.assertEqual(response.status_code, 403)


class LiveServerTest(LIVE_SERVER_CLASS):
    """Abstract class with helpers from django/contrib/admin/tests.py """
    fixtures = ["autocomplete/initial.json"]

    @classmethod
    def setUpClass(cls):
        cls.selenium = WebDriver()
        super(LiveServerTest, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super(LiveServerTest, cls).tearDownClass()

    def setUp(self):
        super(LiveServerTest, self).setUp()

    def wait_for_ajax(self):
        while self.selenium.execute_script("return jQuery.active != 0"):
            time.sleep(0.1)

    # this bits from Django
    # https://github.com/django/django/blob/master/django/contrib/admin/tests.py#L36
    def wait_until(self, callback, timeout=10):
        from selenium.webdriver.support.wait import WebDriverWait
        WebDriverWait(self.selenium, timeout).until(callback)

    def wait_for_popup(self, num_windows=2, timeout=10):
        self.wait_until(lambda d: len(d.window_handles) == num_windows, timeout)

    def wait_page_loaded(self, by=By.TAG_NAME, search="body"):
        from selenium.webdriver.support.wait import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        WebDriverWait(self.selenium, 5).until(
            EC.presence_of_element_located((by, search))
        )

    def admin_login(self, username, password, login_url='/admin/'):
        self.selenium.get('%s%s' % (self.live_server_url, login_url))
        username_input = self.selenium.find_element("name", 'username')
        username_input.send_keys(username)
        password_input = self.selenium.find_element("name", 'password')
        password_input.send_keys(password)
        login_text = 'Log in'
        self.selenium.find_element("xpath",
            '//input[@value="%s"]' % login_text).click()
        self.wait_page_loaded(By.CLASS_NAME, "dashboard")


@override_settings(ROOT_URLCONF="autocomplete.urls")
class YaaacLiveServerTest(LiveServerTest):
    def test_foreign_key_autocomplete(self):
        mick = models.BandMember.objects.create(first_name="Mick", last_name="Jagger")
        self.selenium.get('%s/band-member-form/%d/' % (self.live_server_url, mick.pk))

        band_search_elem = self.selenium.find_element("xpath", '//input[@class="yaaac_search_input"]')
        self.assertTrue(band_search_elem.is_displayed())
        band_search_elem.send_keys("the ")
        self.wait_for_ajax()
        suggestion_elems = self.selenium.find_elements('class name', 'autocomplete-suggestion')
        self.assertEqual(len(suggestion_elems), 3)
        self.assertEqual([elem.text for elem in suggestion_elems],
                         [u"The Rolling Stones (Blues/Rock)", u"The Stone Roses (Rock)", "The Bee Gees (Cheese)"])

        suggestion_elems[0].click()
        self.assertEqual(self.selenium.find_element("id", 'id_band').get_attribute("value"), "2")
        WebDriverWait(self.selenium, 2).until(EC.invisibility_of_element_located((By.ID, "lookup_id_band")))
        self.assertFalse(band_search_elem.is_displayed())

        band_value_container = self.selenium.find_element("class name", 'yaaac_value_container')
        self.assertTrue(band_value_container.is_displayed())
        band_value_elem = self.selenium.find_element("class name", 'yaaac_value')
        self.assertEqual(band_value_elem.text, "The Rolling Stones")

        # Clear the choice.
        self.selenium.find_element("class name", 'yaaac_clear_value').click()
        self.assertEqual(self.selenium.find_element("id", 'id_band').get_attribute("value"), "")
        self.assertTrue(band_search_elem.is_displayed())
        self.assertFalse(band_value_container.is_displayed())

    def test_foreign_key_autocomplete_with_initial(self):
        mick = models.BandMember.objects.create(first_name="Mick", last_name="Jagger", band_id=2)
        self.selenium.get('%s/band-member-form/%d/' % (self.live_server_url, mick.pk))

        # The autocomplete field is not visible.
        band_search_elem = self.selenium.find_element("xpath", '//input[@class="yaaac_search_input"]')
        self.assertFalse(band_search_elem.is_displayed())

        # But the label is.
        band_value_container = self.selenium.find_element("class name", 'yaaac_value_container')
        self.assertTrue(band_value_container.is_displayed())
        band_value_elem = self.selenium.find_element("class name", 'yaaac_value')
        self.assertEqual(band_value_elem.text, "The Rolling Stones")

    def test_foreign_key_related_lookup(self):
        self.admin_login("super", "secret", login_url='/admin/')
        mick = models.BandMember.objects.create(first_name="Mick", last_name="Jagger")

        self.selenium.get('%s/band-member-form/%d/' % (self.live_server_url, mick.pk))
        main_window = self.selenium.current_window_handle
        self.selenium.find_element("class name", 'yaaac_lookup').click()

        self.wait_for_popup()
        self.selenium.switch_to.window(self.selenium.window_handles[1])
        self.selenium.find_element("link text", "SuperHeavy").click()
        self.selenium.switch_to.window(main_window)
        self.assertEqual(self.selenium.find_element("id", 'id_band').get_attribute("value"), "4")

        # The autocomplete field is now hidden.
        band_search_elem = self.selenium.find_element("xpath", '//input[@class="yaaac_search_input"]')
        WebDriverWait(self.selenium, 2).until(EC.invisibility_of_element_located(
            (By.XPATH, '//input[@class="yaaac_search_input"]')))
        self.assertFalse(band_search_elem.is_displayed())

        # And the label is shown.
        band_value_container = self.selenium.find_element("class name", 'yaaac_value_container')
        self.assertTrue(band_value_container.is_displayed())
        band_value_elem = self.selenium.find_element("class name", 'yaaac_value')
        self.assertEqual(band_value_elem.text, "SuperHeavy")

    def test_foreign_key_limit_choices_autocomplete(self):
        mick = models.BandMember.objects.create(first_name="Mick", last_name="Jagger")
        self.selenium.get('%s/band-member-form/limit-choices/%d/' % (self.live_server_url, mick.pk))

        band_search_elem = self.selenium.find_element("xpath", '//input[@class="yaaac_search_input"]')
        self.assertTrue(band_search_elem.is_displayed())
        band_search_elem.send_keys("the ")
        self.wait_for_ajax()
        suggestion_elems = self.selenium.find_elements('class name', 'autocomplete-suggestion')
        self.assertEqual(len(suggestion_elems), 2)
        self.assertEqual([elem.text for elem in suggestion_elems],
                         [u"The Rolling Stones", u"The Stone Roses"])

        suggestion_elems[0].click()
        self.assertEqual(self.selenium.find_element("id", 'id_band').get_attribute("value"), "2")
        WebDriverWait(self.selenium, 2).until(EC.invisibility_of_element_located(
            (By.XPATH, '//input[@class="yaaac_search_input"]')))
        self.assertFalse(band_search_elem.is_displayed())

        band_value_container = self.selenium.find_element("class name", 'yaaac_value_container')
        self.assertTrue(band_value_container.is_displayed())
        band_value_elem = self.selenium.find_element("class name", 'yaaac_value')
        self.assertEqual(band_value_elem.text, "The Rolling Stones")

        # Clear the choice.
        self.selenium.find_element("class name", 'yaaac_clear_value').click()
        self.assertEqual(self.selenium.find_element("id", 'id_band').get_attribute("value"), "")
        self.assertTrue(band_search_elem.is_displayed())
        self.assertFalse(band_value_container.is_displayed())

    def test_foreign_key_limit_choices_related_lookup(self):
        self.admin_login("super", "secret", login_url='/admin/')
        mick = models.BandMember.objects.create(first_name="Mick", last_name="Jagger")

        self.selenium.get('%s/band-member-form/limit-choices/%d/' % (self.live_server_url, mick.pk))
        main_window = self.selenium.current_window_handle
        self.selenium.find_element("class name", 'yaaac_lookup').click()

        self.wait_for_popup()
        self.selenium.switch_to.window(self.selenium.window_handles[1])
        self.selenium.find_element("link text", "SuperHeavy").click()
        self.selenium.switch_to.window(main_window)
        self.assertEqual(self.selenium.find_element("id", 'id_band').get_attribute("value"), "4")

        # The autocomplete field is now hidden.
        band_search_elem = self.selenium.find_element("xpath", '//input[@class="yaaac_search_input"]')
        WebDriverWait(self.selenium, 2).until(EC.invisibility_of_element_located(
            (By.XPATH, '//input[@class="yaaac_search_input"]')))
        self.assertFalse(band_search_elem.is_displayed())

        # And the label is shown.
        band_value_container = self.selenium.find_element("class name", 'yaaac_value_container')
        self.assertTrue(band_value_container.is_displayed())
        band_value_elem = self.selenium.find_element("class name", 'yaaac_value')
        self.assertEqual(band_value_elem.text, "SuperHeavy")

    def test_extra_css(self):
        self.admin_login("super", "secret", login_url='/admin/')
        self.selenium.get('%s/band-member-form/extra-css/' % self.live_server_url)
        container = self.selenium.find_element("class name", 'yaaac_container')
        self.assertEqual(container.get_attribute('class'), u'yaaac_container my_extra_class')

    def test_no_lookup(self):
        from selenium.common.exceptions import NoSuchElementException
        self.admin_login("super", "secret", login_url='/admin/')
        self.selenium.get('%s/band-member-form/no-lookup/' % self.live_server_url)
        self.assertRaises(NoSuchElementException, self.selenium.find_element, 'class name', 'yaaac_lookup')
