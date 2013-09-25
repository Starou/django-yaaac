import json
from django.contrib.auth.models import User
from django.test import TestCase
from django.test.client import Client


class AutocompleteTest(TestCase):
    def setUp(self):
        super(AutocompleteTest, self).setUp()
        self.client = Client()
    
    def test_search(self):
       response = self.client.get("/yaaac/7/search/?query=gene") 
       self.assertEqual(json.loads(response.content),
                        {u'data': [1], u'query': u'gene', u'suggestions': [u'Genesis']})
