# -*- coding: utf-8 -*-

import unittest


class UtilsTestCase(unittest.TestCase):
    def test_lookup_dict_from_url_params(self):
        from django_yaaac.utils import lookup_dict_from_url_params
        self.assertEqual(lookup_dict_from_url_params({"genre__name__in": "Rock,Blues/Rock",
                                                      "label__name": "Foo Records"}),
                         {"genre__name__in": ["Rock","Blues/Rock"],
                          "label__name": "Foo Records"})


def suite():
    suite = unittest.TestLoader().loadTestsFromTestCase(UtilsTestCase)
    return suite
