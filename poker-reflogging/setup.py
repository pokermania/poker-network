#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from distutils.core import setup
sys.path.append('../common')
from setup_extensions import TestCommand

setup(
    name = 'reflogging',
    version = '1.0.0',
    packages = ['reflogging'],
    cmdclass = {'test': TestCommand}
)
