import unittest

import omise


class ProductionUrlsTest(unittest.TestCase):
    def test_api_urls_match_production_endpoints(self):
        self.assertEqual(omise.api_main, 'https://api.omise.co')
        self.assertEqual(omise.api_vault, 'https://vault.omise.co')