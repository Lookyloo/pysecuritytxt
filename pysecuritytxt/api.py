#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import ipaddress
import json
import logging
import re

from typing import Set, Union, Dict, List
from urllib.parse import urljoin, urlparse

import requests


class PySecurityTXTException(Exception):
    pass


class SecurityTXTNotAvailable(PySecurityTXTException):
    pass


class PySecurityTXT():

    def __init__(self, loglevel: int=logging.INFO):
        """Do things to a security.txt file."""
        self.logger = logging.getLogger(f'{self.__class__.__name__}')
        self.logger.setLevel(loglevel)
        self.session = requests.session()
        self.expected_paths = ['/.well-known/security.txt', '/security.txt']

    def _try_get_url(self, url: str) -> str:
        try:
            response = self.session.get(url)
            response.raise_for_status()
        except (requests.HTTPError, requests.exceptions.ConnectionError):
            raise SecurityTXTNotAvailable(f'Unable to get the file from: {url}')
        return response.text

    def _all_possible_domains(self, hostname: str) -> Set[str]:
        hostname_parts = hostname.split('.')
        if len(hostname_parts) <= 2:
            return {hostname, }
        current_domain = '.'.join(hostname_parts[-2:])
        to_return: Set[str] = {current_domain, }
        for domain_part in reversed(hostname_parts[:-2]):
            current_domain = f'{domain_part}.{current_domain}'
            to_return.add(current_domain)
        return to_return

    def parse(self, file: str) -> Dict[str, Union[str, List[str]]]:
        """Takes a security.txt file, parses it.

            :param file: The security.txt file.
        """
        to_return = {}
        if acknowledgments := re.findall("^[A,a]cknowledgments[:]? (.*)$", file, re.MULTILINE):
            if len(acknowledgments) == 1:
                to_return['acknowledgments'] = acknowledgments[0]
            else:
                to_return['acknowledgments'] = acknowledgments
        if canonical := re.findall("^[C,c]canonical[:]? (.*)$", file, re.MULTILINE):
            if len(canonical) == 1:
                to_return['canonical'] = canonical[0]
            else:
                to_return['canonical'] = canonical
        if contact := re.findall("^[C,c]ontact[:]? (.*)$", file, re.MULTILINE):
            if len(contact) == 1:
                to_return['contact'] = contact[0]
            else:
                to_return['contact'] = contact
        if encryption := re.findall("^[E,e]ncryption[:]? (.*)$", file, re.MULTILINE):
            if len(encryption) == 1:
                to_return['encryption'] = encryption[0]
            else:
                to_return['encryption'] = encryption
        if expires := re.findall("^[E,e]xpires[:]? (.*)$", file, re.MULTILINE):
            if len(expires) == 1:
                to_return['expires'] = expires[0]
            else:
                to_return['expires'] = expires
        if hiring := re.findall("^[H,h]iring[:]? (.*)$", file, re.MULTILINE):
            if len(hiring) == 1:
                to_return['hiring'] = hiring[0]
            else:
                to_return['hiring'] = hiring

        if policy := re.findall("^[P,p]olicy[:]? (.*)$", file, re.MULTILINE):
            if len(policy) == 1:
                to_return['policy'] = policy[0]
            else:
                to_return['policy'] = policy
        if prefered_languages := re.findall("^[P,p]referred-[L,l]anguages[:]? (.*)$", file, re.MULTILINE):
            # this one must be there only once, and contains a list of languages
            # I have limited trust on that, so let's normalize it
            languages: List[str] = []
            for lang_list in prefered_languages:
                languages += [language.strip() for language in lang_list.split(',') if language.strip()]
            to_return['prefered-languages'] = languages
        return to_return

    def get(self, hint: str, /, *, parse: bool=False) -> str:
        '''Get the security.txt file.

            :param hint: It can be a domain, an IP or an URL (and we try to figure out where the file is), or a full URL to the file.
            :param parse: Parse the file and returns a json dictionary with the relevant fields
        '''
        if hint.endswith('security.txt'):
            response = self._try_get_url(hint)
            if parse:
                return json.dumps(self.parse(response))
            return response

        if re.search("^http[s]?://", hint):
            # we have a URL, get the hostname
            splitted_url = urlparse(hint)
            if not (hostname := splitted_url.hostname):
                raise PySecurityTXTException(f'Unable to get a hostname out of the hint: {hint}')
        else:
            hostname = hint

        try:
            ipaddress.ip_address(hostname)
            all_domains = {hostname, }
            ip = True
        except ValueError:
            all_domains = self._all_possible_domains(hostname)
            ip = False
        test_urls: Set[str] = set()
        for domain in all_domains:
            # we have what should be a domain or an ip, let's try a few things
            for expected_path in self.expected_paths:
                test_urls.update([
                    urljoin(f'https://{domain}', expected_path),
                    urljoin(f'http://{domain}', expected_path)
                ])

            if not domain.startswith('www') and not ip:
                for expected_path in self.expected_paths:
                    test_urls.update([
                        urljoin(f'https://www.{domain}', expected_path),
                        urljoin(f'http://www.{domain}', expected_path)
                    ])

        for url in sorted(test_urls, key=len, reverse=True):  # Longest URL first, so /.well-known/ path is prioritized
            try:
                response = self._try_get_url(url)
                if re.search("^[C,c]ontact", response, re.MULTILINE):
                    # Because we often get responses that are just plain HTML pages and a 2XX status code.
                    break
            except SecurityTXTNotAvailable:
                self.logger.debug(f'Not available on {url}')
        else:
            raise SecurityTXTNotAvailable(f'Unable to file on {", ".join(test_urls)}')

        if not parse:
            return response
        return json.dumps(self.parse(response))
