#!/usr/bin/env python
# -*- coding: utf-8 -*-

from distutils.core import Command
import os, tests, sys
import unittest

class TestCommand(Command):
    user_options = [ ]

    def initialize_options(self):
        self._dir = os.getcwd()

    def finalize_options(self):
        pass

    def run(self):
        """
        Finds all the tests modules in tests/, and runs them.
        """
        unittest.installHandler()
        for mod_name, mod in tests.__dict__.items():
            if mod_name.startswith('test_'):
                print "\n"+mod_name
                runner = unittest.TextTestRunner(verbosity=1, failfast=True)
                result = runner.run(mod.GetTestSuite())
                if len(result.failures) > 0 or len(result.errors) > 0:
                    sys.exit(1)

import re
from config import config
from glob import glob

class ConfigureCommand(Command):
    user_options = [ ]

    def initialize_options(self):
        self._dir = os.getcwd()

    def finalize_options(self):
        pass

    def run(self):
        """
        Finds all .in files and execute replacements
        """
        _re = re.compile(r"@([a-zA-Z\._]*)@")

        for _file in glob('*.in') + glob('*/*.in') + glob('*/*/*.in'):
            _out_file = _file[:-3]
            print _file, '->', _out_file
            _fd_i = open(_file, 'r')
            _fd_o = open(_out_file, 'w')
            try:
                _fd_o.write(_re.sub(lambda m: str(eval(m.group(1), {
                    'version': self.distribution.get_version(),
                    'srcdir': os.getcwd(),
                    'config': config
                })), _fd_i.read()))
            except NameError as e:
                e.args = (e.args[0]+" (is looked up in config)",)
                raise

