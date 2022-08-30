#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging

from typing import List
from urllib.parse import urljoin

import requests


class PySecurityTXTException(Exception):
    pass


class SecurityTXTNotAvailable(PySecurityTXTException):
    pass


class PySecurityTXT():

    def __init__(self, loglevel: int=logging.INFO):
        self.logger = logging.getLogger(f'{self.__class__.__name__}')
        self.logger.setLevel(loglevel)
        self.session = requests.session()
        self.expected_path = '/.well-known/security.txt'

    def _try_get_url(self, url: str) -> str:
        response = self.session.get(url)
        try:
            response.raise_for_status()
        except requests.HTTPError:
            raise SecurityTXTNotAvailable(f'Unable to get the file from: {url}')
        return response.text

    def get(self, hint: str, /) -> str:
        '''Get the security.txt file.
        :param hint: It can be a domain (and we try to figureout wher ethe file is, or a full URL to the file.
        '''
        if hint.endswith('security.txt'):
            return self._try_get_url(hint)
        # we have what should be a domain, let's try a few things
        test_urls: List[str] = [
            urljoin(f'https://{hint}', self.expected_path),
            urljoin(f'http://{hint}', self.expected_path)
        ]
        if not hint.startswith('www'):
            test_urls += [
                urljoin(f'https://www.{hint}', self.expected_path),
                urljoin(f'http://www.{hint}', self.expected_path)
            ]
        for url in test_urls:
            try:
                response = self._try_get_url(url)
                break
            except SecurityTXTNotAvailable:
                self.logger.debug(f'Not available on {url}')
        else:
            raise SecurityTXTNotAvailable(f'Unable to file on {", ".join(test_urls)}')

        return response
