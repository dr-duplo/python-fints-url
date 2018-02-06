from unittest import TestCase

from urllib.parse import urlparse
import fints_url

class TestBasics(TestCase):
    def test_bank_codes(self):
        for bc in [86055592, 10077777, 10070000, 43060967]:
            url = fints_url.find(bank_code=bc)
            assert urlparse(url)
