import argparse

from .api import PySecurityTXT


def main():
    parser = argparse.ArgumentParser(description='Try to get a security.txt file')
    parser.add_argument('url_or_domain', help='Try to get the file from there.')
    args = parser.parse_args()

    client = PySecurityTXT()
    response = client.get(args.url_or_domain)
    print(response)
