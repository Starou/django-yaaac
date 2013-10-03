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
       response = self.client.get("/yaaac/7/search/?query=gene&value_attr=name") 
       self.assertEqual(json.loads(response.content),
                        {u'query': u'gene', u'suggestions': [{u'data': 1, u'value': u'Genesis'}]})

    def test_search_with_pk(self):
       response = self.client.get("/yaaac/7/search/?pk=1") 
       self.assertEqual(json.loads(response.content), {'value': 'Genesis'})

class LiveServerTest(LiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        cls.selenium = WebDriver()
        super(LiveServerTest, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        super(LiveServerTest, cls).tearDownClass()
        cls.selenium.quit()

    def setUp(self):
        super(LiveServerTest, self).setUp()

    def wait_for_ajax(self):
        while self.selenium.execute_script("return jQuery.active != 0"):
            time.sleep(0.1)

    def test_foreign_key_autocomplete(self):
        mick = models.BandMember.objects.create(first_name="Mick", last_name="Jagger")

        self.selenium.get('%s/%d/' % (self.live_server_url, mick.pk))
        band_search_elem = self.selenium.find_element_by_xpath('//input[@class="yaaac_search_input"]')
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
