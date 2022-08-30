#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest

from pysecuritytxt import PySecurityTXT


class TestBasic(unittest.TestCase):

    def setUp(self):
        self.client = PySecurityTXT()

    def test_basic(self):
        txt = self.client.get('circl.lu')
        self.assertTrue(txt)
