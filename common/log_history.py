# -*- coding: utf-8 *-*

import logging
from collections import namedtuple

Message = namedtuple('Message', ['severity', 'path', 'refs', 'message', 'args', 'formated'])

logging.getLogger().setLevel(logging.DEBUG)

class TestLoggingHandler(logging.Handler):

    def __init__(self, log, level=logging.DEBUG):
        self.log = log
        logging.Handler.__init__(self, level=level)

    def emit(self, record):
        self.log.output.append(Message(
            severity = record.levelno,
            path = record.name,
            refs = record.refs if hasattr(record, 'refs') else '[]',
            message = record.msg,
            args = record.args,
            formated = self.format(record)
        ))

class Log(object):

    def __init__(self, logger=None):
        self.reset()
        self.handler = TestLoggingHandler(self)
        self.logger = logger if logger else logging.getLogger()
        self.logger.addHandler(self.handler)

    def __del__(self):
        self.unregister()

    def unregister(self):
        self.logger.removeHandler(self.handler)

    def reset(self):
        self.output = []

    def get_all(self):
        return [m.formated for m in self.output]

    def search(self, needle):
        for m in self.output:
            if needle in m.formated:
                return True
        return False



