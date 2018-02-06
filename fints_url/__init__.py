import requests
from lxml import html
from schwifty import IBAN
from urllib.parse import urlparse
import logging

log = logging.getLogger( "fints-url" )

# url used to search for a bank code to obtain a bank key
BANK_SELECT_URL = 'https://www.hbci-zka.de/institute/institut_select.php'
# url to get bank details using the bank key
BANK_DETAIL_URL = 'https://www.hbci-zka.de/institute/institut_detail.php'

def __find_bank_key(bank_code):
    payload = {
        'blz_search' : str(bank_code)
    }

    response = requests.post(BANK_SELECT_URL, data=payload)

    html_tree = html.fromstring(response.content)

    options = html_tree.xpath('//form[@name="Bankenselektion"]/table[1]/tr')

    for o in options:
        if str(bank_code) == o.xpath('td[2]/text()')[0].strip():
            return int(o.xpath('td[1]/input/@value')[0].strip())

    raise Exception("Bank with bank code %s not found!" % bank_code)

def __get_fints_url(bank_key):
    payload = {
        'blz_auswahl_radio' : bank_key
    }

    response = requests.post(BANK_DETAIL_URL, data=payload)

    html_tree = html.fromstring(response.content)
    bank_url = html_tree.xpath('//tr/td[contains(text(),"PIN/TAN URL:")]/following-sibling::td/text()')[0].strip()

    return bank_url

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

    key = __find_bank_key(bank_code)
    url = urlparse(__get_fints_url(key)).geturl()

    log.debug("FinTS URL for IBAN=%s bank_code=%s: (%u) %s" % (iban, bank_code, key, url))

    return url
