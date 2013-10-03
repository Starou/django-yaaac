import json
from django.contrib.auth.models import User
from django.test import TestCase, LiveServerTestCase
from django.test.client import Client
from selenium.webdriver.firefox.webdriver import WebDriver


class AutocompleteTest(TestCase):
    def setUp(self):
        super(AutocompleteTest, self).setUp()
        self.client = Client()
    
    def test_search(self):
       response = self.client.get("/yaaac/7/search/?query=gene&value_attr=name") 
       self.assertEqual(json.loads(response.content),
                        {u'query': u'gene', u'suggestions': [{u'data': 1, u'value': u'Genesis'}]})


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

    def test_foreign_key_autocomplete(self):
        self.selenium.get('%s/' % self.live_server_url)
        band_input = self.selenium.find_element_by_name("band")
        band_input.send_keys("the ")
        import ipdb
        ipdb.set_trace()
