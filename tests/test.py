#!/usr/bin/env python3

import unittest

from pysecuritytxt import PySecurityTXT


class TestBasic(unittest.TestCase):

    def setUp(self) -> None:
        self.client = PySecurityTXT()

    def test_basic(self) -> None:
        txt = self.client.get('circl.lu')
        self.assertTrue(txt)

    def test_securitytxt_in_root(self) -> None:
        txt = self.client.get('liu.se')
        self.assertTrue(txt)

    def test_field_csaf(self) -> None:
        txt = self.client.get('https://www.cisa.gov/sites/default/files/security.txt', parse=True)
        self.assertTrue('csaf' in txt)
