import argparse

from .api import PySecurityTXT, SecurityTXTNotAvailable  # noqa


def main():
    parser = argparse.ArgumentParser(description='Try to get a security.txt file')
    parser.add_argument('url_or_domain', help='Try to get the file from there.')
    parser.add_argument('-p', '--parse', default=False, action='store_true', help='Parse the response, returns dict')
    args = parser.parse_args()

    client = PySecurityTXT()
    response = client.get(args.url_or_domain, parse=args.parse)
    print(response)
