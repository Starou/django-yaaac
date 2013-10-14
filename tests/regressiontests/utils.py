# -*- coding: utf-8 -*-

import unittest


class UtilsTestCase(unittest.TestCase):
    def test_lookup_dict_from_url_params(self):
        from django_yaaac.utils import lookup_dict_from_url_params
        self.assertEqual(lookup_dict_from_url_params({"genre__name__in": "Rock,Blues/Rock",
                                                      "label__name": "Foo Records"}),
                         {"genre__name__in": ["Rock","Blues/Rock"],
                          "label__name": "Foo Records"})

    def test_clean_fieldname_prefix(self):
        from django_yaaac.utils import clean_fieldname_prefix
        self.assertEqual(clean_fieldname_prefix("name"), "name")
        self.assertEqual(clean_fieldname_prefix("prefix-form-1-name"), "name")
        self.assertEqual(clean_fieldname_prefix("prefix_form-1-name"), "name")
        self.assertEqual(clean_fieldname_prefix("prefixform-1-name"), "name")


def suite():
    suite = unittest.TestLoader().loadTestsFromTestCase(UtilsTestCase)
    return suite
