from . import find
import argparse

def main():
    parser = argparse.ArgumentParser(description="Find FinTS URL of a german bank")
    parser.add_argument('--iban', '-i', type=str, help='German IBAN of an account at the bank.')
    parser.add_argument('--bank-code', '-b', type=str, help='German bank code.')

    args = parser.parse_args()

    print(find(iban=args.iban, bank_code=args.bank_code))
