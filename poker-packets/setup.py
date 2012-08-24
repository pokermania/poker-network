#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from distutils.core import setup
sys.path.append('../common')
from setup_ext.test import TestCommand

setup(
    name = 'poker-packets',
    version = '2.2.0',
    packages = ['pokerpackets'],
    cmdclass = {'test': TestCommand}
)
