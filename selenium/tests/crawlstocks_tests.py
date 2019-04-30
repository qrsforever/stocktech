#!/usr/bin/python3
# -*- coding: utf-8 -*-

from nose.toolsimport *
import crawlstocks

def setup():
    print("SETUP!")

def teardown():
    print("TEAR DOWN!")

def test_basic():
   print("I RAN!")
