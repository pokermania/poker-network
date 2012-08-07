#!/usr/bin/env python
# -*- coding: utf-8 -*-

from distutils.core import Command
import os, tests, sys
import unittest

class TestCommand(Command):
    user_options = []

    def initialize_options(self):
        self._dir = os.getcwd()

    def finalize_options(self):
        pass

    def run(self):
        """
        Finds all the tests modules in tests/, and runs them.
        """
        for mod_name, mod in tests.__dict__.items():
            if mod_name.startswith('test_'):
                print "\n"+mod_name
                runner = unittest.TextTestRunner(verbosity=1)
                result = runner.run(mod.GetTestSuite())
                if len(result.failures) > 0 or len(result.errors) > 0:
                    sys.exit(1)

