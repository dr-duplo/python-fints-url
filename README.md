# German Bank FinTS Url Finder
This is a python module that can be used to obtain the FinTS URL of german banks.
As of my knowledge, there's no public available API to request them.

The module uses the bank info database of aqbanking at
https://github.com/aqbanking/aqbanking/raw/master/src/plugins/bankinfo/generic/de.tar.bz2.

## Usage
The module can be used as standalone script or library.

### Installation
```
pip3 install fints-url
```

### Command Line Interface
```
$ fints-url --help
usage: fints-url [-h] [--iban IBAN] [--bank-code BANK_CODE]

Find FinTS URL of a german bank

optional arguments:
  -h, --help            show this help message and exit
  --iban IBAN, -i IBAN  German IBAN of an account at the bank.
  --bank-code BANK_CODE, -b BANK_CODE
                        German bank code.
```

```
$ fints-url -b 86055592
https://banking-sn5.s-fints-pt-sn.de/fints30
```
### Library Usage
```
import fints_url

url = fints_url.find(bank_code=86055592)
```
## Status
This is an early version. Please report errors/bugs.

## Licensing
MIT License
