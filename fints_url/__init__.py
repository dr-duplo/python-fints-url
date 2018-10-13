import requests
from lxml import html
from schwifty import IBAN
from urllib.parse import urlparse
import logging
import pickle
import os

log = logging.getLogger( "fints-url" )

# load bank info
with open(os.path.join(os.path.dirname(__file__), 'bank_info.pickle'), 'rb') as f:
    __bank_info__ = pickle.load(f)

def find(iban = None, bank_code = None):
    """Find FinTS URL for a german bank.

    Keyword arguments:
    iban -- a valid german IBAN (overrides bank_code)
    bank_code -- a valid german bank code (fallback if iban not provided)
    """

    if iban:
        iban = IBAN(iban) if not isinstance(iban, IBAN) else iban

        if iban.country_code != 'DE':
            raise Exception("FinTS is supported by german banks only!")

        bank_code = iban.bank_code

    if not bank_code:
        raise Exception("Please provide IBAN or bank code!")

    try:
        url = __bank_info__[str(bank_code)]['fints']
    except:
        raise Exception("FinTS URL not found for %s" % str(bank_code))

    log.debug("FinTS URL for IBAN=%s bank_code=%s: %s" % (iban, bank_code, url))

    return url
