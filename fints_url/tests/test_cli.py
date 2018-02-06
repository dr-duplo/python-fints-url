from unittest import TestCase

from urllib.parse import urlparse
from fints_url.cli import main
from mock import patch
import sys

class TestBasics(TestCase):
    def test_cli(self):
        for bc in [86055592, 10077777, 10070000, 43060967]:
            testargs = ['foo', '-b', str(bc)]
            with patch.object(sys, 'argv', testargs):
                main()
