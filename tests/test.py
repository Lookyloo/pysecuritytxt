#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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
