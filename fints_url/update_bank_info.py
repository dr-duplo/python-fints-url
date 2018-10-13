import requests, io, os, tarfile, re, urllib, pickle
from enum import Enum

def update():

    print('Fetching aqbanking DB...')
    response = requests.get("https://github.com/aqbanking/aqbanking/raw/master/src/plugins/bankinfo/generic/de.tar.bz2")
    tar_bz2_obj = io.BytesIO(response.content)

    print('Parsing fints data...')

    tar = tarfile.open(fileobj=tar_bz2_obj)
    f = tar.extractfile(member='de/banks.data')

    re_blank = r"^\s*$"
    re_bank_id = r"^bankId=\"(\d+)\""
    re_bank_name = r"^bankName=\"([^\"]+)\""
    re_element_open = r"\s+element {"
    re_element_close = r"\s+}"
    re_hbci = r"\s+type=\"HBCI\""
    re_pversion = r"\s+pversion=\"([^\"]+)\""
    re_address = r"\s+address=\"([^\"]+)\""
    re_mode = r"\s+mode=\"([^\"]+)\""

    prev_blz = None
    blz = None
    bank_name = None
    hbci_address = None
    hbci_version = None
    hbci_mode = None

    class ParserState(Enum):
        NEXT = 1,
        BANKID = 2,
        BANKNAME = 3,
        ELEMENT_OPEN = 4,
        HBCI = 5,
        ADDRESS = 6,
        PVERSION = 7
        MODE = 8
        ELEMENT_CLOSE = 9,


    bank_data = dict()

    state = ParserState.NEXT
    for line in f:
        line = line.decode("utf-8")

        if re.match(re_blank, line):
            state = ParserState.NEXT
            continue

        if state == ParserState.NEXT:
            blz = None
            bank_name = None
            hbci_mode = None
            hbci_address = None
            hbci_version = None
            matches = re.search(re_bank_id, line)
            if matches:
                blz = matches.group(1)
                if prev_blz != blz:
                    state = ParserState.BANKID

        elif state == ParserState.BANKID:
            matches = re.search(re_bank_name, line)
            if matches:
                bank_name = urllib.parse.unquote(matches.group(1))
                state = ParserState.ELEMENT_OPEN

        elif state == ParserState.ELEMENT_OPEN:
            if re.match(re_element_open, line):
                state = ParserState.HBCI

        elif state == ParserState.HBCI:
            if re.match(re_hbci, line):
                state = ParserState.ELEMENT_CLOSE

        elif state == ParserState.ELEMENT_CLOSE:
            if hbci_version is None:
                matches = re.search(re_pversion, line)
                if matches:
                    hbci_version = (matches.group(1) == '3.0')
                    continue

            if hbci_mode is None:
                matches = re.search(re_mode, line)
                if matches:
                    hbci_mode = (matches.group(1) == 'PINTAN')
                    continue

            if hbci_address is None:
                matches = re.search(re_address, line)
                if matches:
                    hbci_address = urllib.parse.unquote(matches.group(1))
                    if 'fints' in hbci_address.lower():
                        hbci_version = True
                    continue

            if re.match(re_element_close, line):
                if hbci_address and hbci_version and hbci_mode:
                    bank_data[blz] = {'blz' : blz, 'name' : bank_name, 'fints' : hbci_address }
                    prev_blz = blz
                    state = ParserState.NEXT
                else:
                    hbci_mode = None
                    hbci_address = None
                    hbci_version = None
                    state = ParserState.ELEMENT_OPEN

    f.close()
    tar.close()

    pickle.dump(bank_data, open(os.path.join(os.path.dirname(__file__), 'bank_info.pickle'), 'wb'))

if __name__ == '__main__':
    update()
