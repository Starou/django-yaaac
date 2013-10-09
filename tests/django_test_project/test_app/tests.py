import json
import time
from django.contrib.auth.models import User
from django.test import TestCase, LiveServerTestCase
from django.test.client import Client
from test_app import models
from selenium.webdriver.firefox.webdriver import WebDriver


class AutocompleteTest(TestCase):
    def setUp(self):
        super(AutocompleteTest, self).setUp()
        self.client = Client()
    
    def test_search(self):
       response = self.client.get("/yaaac/8/search/?t=id&query=gene&value_attr=name") 
       self.assertEqual(json.loads(response.content),
                        {u'query': u'gene', u'suggestions': [{u'data': 1, u'value': u'Genesis'}]})

    def test_search_with_pk(self):
       response = self.client.get("/yaaac/8/search/?pk=1") 
       self.assertEqual(json.loads(response.content), {'value': 'Genesis'})


class LiveServerTest(LiveServerTestCase):
    """Abstract class with helpers from django/contrib/admin/tests.py """
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

    def wait_until(self, callback, timeout=10):
        from selenium.webdriver.support.wait import WebDriverWait
        WebDriverWait(self.selenium, timeout).until(callback)

    def wait_loaded_tag(self, tag_name, timeout=10):
        self.wait_until(
            lambda driver: driver.find_element_by_tag_name(tag_name),
            timeout
        )

    def wait_page_loaded(self):
        from selenium.common.exceptions import TimeoutException
        try:
            # Wait for the next page to be loaded
            self.wait_loaded_tag('body')
        except TimeoutException:
            # IE7 occasionnally returns an error "Internet Explorer cannot
            # display the webpage" and doesn't load the next page. We just
            # ignore it.
            pass

    def admin_login(self, username, password, login_url='/admin/'):
        self.selenium.get('%s%s' % (self.live_server_url, login_url))
        username_input = self.selenium.find_element_by_name('username')
        username_input.send_keys(username)
        password_input = self.selenium.find_element_by_name('password')
        password_input.send_keys(password)
        login_text = 'Log in'
        self.selenium.find_element_by_xpath(
            '//input[@value="%s"]' % login_text).click()
        self.wait_page_loaded()

            
class YaaacLiveServerTest(LiveServerTest):
    def test_foreign_key_autocomplete(self):
        mick = models.BandMember.objects.create(first_name="Mick", last_name="Jagger")
        self.selenium.get('%s/band-member-form/%d/' % (self.live_server_url, mick.pk))

        band_search_elem = self.selenium.find_element_by_xpath('//input[@class="yaaac_search_input"]')
        self.assertTrue(band_search_elem.is_displayed())
        band_search_elem.send_keys("the ")
        self.wait_for_ajax()
        suggestion_elems = self.selenium.find_elements_by_class_name('autocomplete-suggestion')
        self.assertEqual(len(suggestion_elems), 3)
        self.assertEqual([elem.text for elem in suggestion_elems],
                         [u"The Rolling Stones", u"The Stone Roses", "The Bee Gees"])

        suggestion_elems[0].click()
        self.assertEqual(self.selenium.find_element_by_id('id_band').get_attribute("value"), "2")
        self.assertFalse(band_search_elem.is_displayed())

        band_value_container = self.selenium.find_element_by_class_name('yaaac_value_container')
        self.assertTrue(band_value_container.is_displayed())
        band_value_elem = self.selenium.find_element_by_class_name('yaaac_value')
        self.assertEqual(band_value_elem.text, "The Rolling Stones")

        # Clear the choice.
        self.selenium.find_element_by_class_name('yaaac_clear_value').click()
        self.assertEqual(self.selenium.find_element_by_id('id_band').get_attribute("value"), "")
        self.assertTrue(band_search_elem.is_displayed())
        self.assertFalse(band_value_container.is_displayed())

    def test_foreign_key_autocomplete_with_initial(self):
        mick = models.BandMember.objects.create(first_name="Mick", last_name="Jagger", band_id=2)
        self.selenium.get('%s/band-member-form/%d/' % (self.live_server_url, mick.pk))

        # The autocomplete field is not visible.
        band_search_elem = self.selenium.find_element_by_xpath('//input[@class="yaaac_search_input"]')
        self.assertFalse(band_search_elem.is_displayed())

        # But the label is.
        band_value_container = self.selenium.find_element_by_class_name('yaaac_value_container')
        self.assertTrue(band_value_container.is_displayed())
        band_value_elem = self.selenium.find_element_by_class_name('yaaac_value')
        self.assertEqual(band_value_elem.text, "The Rolling Stones")

    def test_foreign_key_related_lookup(self):
        self.admin_login("super", "secret", login_url='/admin/')
        mick = models.BandMember.objects.create(first_name="Mick", last_name="Jagger")

        self.selenium.get('%s/band-member-form/%d/' % (self.live_server_url, mick.pk))
        main_window = self.selenium.current_window_handle
        self.selenium.find_element_by_class_name('yaaac_lookup').click()

        self.selenium.switch_to_window('id_band')
        self.wait_page_loaded()
        
        band_link = self.selenium.find_element_by_xpath("//tr[3]//a")
        self.assertEqual(band_link.text, "SuperHeavy")
        band_link.click()
        self.selenium.switch_to_window(main_window)
        self.assertEqual(self.selenium.find_element_by_id('id_band').get_attribute("value"), "4")

        # The autocomplete field is now hidden.
        band_search_elem = self.selenium.find_element_by_xpath('//input[@class="yaaac_search_input"]')
        self.assertFalse(band_search_elem.is_displayed())

        # And the label is shown.
        band_value_container = self.selenium.find_element_by_class_name('yaaac_value_container')
        self.assertTrue(band_value_container.is_displayed())
        band_value_elem = self.selenium.find_element_by_class_name('yaaac_value')
        self.assertEqual(band_value_elem.text, "SuperHeavy")

    def test_foreign_key_limit_choices_autocomplete(self):
        mick = models.BandMember.objects.create(first_name="Mick", last_name="Jagger")
        self.selenium.get('%s/band-member-form/limit-choices/%d/' % (self.live_server_url, mick.pk))

        band_search_elem = self.selenium.find_element_by_xpath('//input[@class="yaaac_search_input"]')
        self.assertTrue(band_search_elem.is_displayed())
        band_search_elem.send_keys("the ")
        self.wait_for_ajax()
        suggestion_elems = self.selenium.find_elements_by_class_name('autocomplete-suggestion')
        self.assertEqual(len(suggestion_elems), 2)
        self.assertEqual([elem.text for elem in suggestion_elems],
                         [u"The Rolling Stones", u"The Stone Roses"])

        suggestion_elems[0].click()
        self.assertEqual(self.selenium.find_element_by_id('id_band').get_attribute("value"), "2")
        self.assertFalse(band_search_elem.is_displayed())

        band_value_container = self.selenium.find_element_by_class_name('yaaac_value_container')
        self.assertTrue(band_value_container.is_displayed())
        band_value_elem = self.selenium.find_element_by_class_name('yaaac_value')
        self.assertEqual(band_value_elem.text, "The Rolling Stones")

        # Clear the choice.
        self.selenium.find_element_by_class_name('yaaac_clear_value').click()
        self.assertEqual(self.selenium.find_element_by_id('id_band').get_attribute("value"), "")
        self.assertTrue(band_search_elem.is_displayed())
        self.assertFalse(band_value_container.is_displayed())

    def test_foreign_key_limit_choices_related_lookup(self):
        self.admin_login("super", "secret", login_url='/admin/')
        mick = models.BandMember.objects.create(first_name="Mick", last_name="Jagger")

        self.selenium.get('%s/band-member-form/limit-choices/%d/' % (self.live_server_url, mick.pk))
        main_window = self.selenium.current_window_handle
        self.selenium.find_element_by_class_name('yaaac_lookup').click()

        self.selenium.switch_to_window('id_band')
        self.wait_page_loaded()
        
        band_link = self.selenium.find_element_by_xpath("//tr[1]//a")
        self.assertEqual(band_link.text, "SuperHeavy")
        band_link.click()
        self.selenium.switch_to_window(main_window)
        self.assertEqual(self.selenium.find_element_by_id('id_band').get_attribute("value"), "4")

        # The autocomplete field is now hidden.
        band_search_elem = self.selenium.find_element_by_xpath('//input[@class="yaaac_search_input"]')
        self.assertFalse(band_search_elem.is_displayed())

        # And the label is shown.
        band_value_container = self.selenium.find_element_by_class_name('yaaac_value_container')
        self.assertTrue(band_value_container.is_displayed())
        band_value_elem = self.selenium.find_element_by_class_name('yaaac_value')
        self.assertEqual(band_value_elem.text, "SuperHeavy")
