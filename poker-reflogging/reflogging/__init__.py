# -*- coding: utf-8 *-*

import logging

class NullHandler(logging.Handler):
    """needed because logging.NullHandler is only available from 2.7 on"""
    def handle(self, record):
        pass
    def emit(self, record):
        pass
    def createLock(self):
        self.lock = None

class Logger(object):
    
    def __init__(self, name, parent=None, refs=[]):
        if parent:
            if isinstance(parent, Logger):
                self._logger = logging.getLogger(".".join((parent._logger.name, name)))
            else:
                self._logger = logging.getLogger(".".join((parent.name, name)))
        else:
            self._logger = logging.getLogger(name)
            # if there is no parent add the nullhandler
            self._logger.addHandler(NullHandler())

        # refs are tuples containing: refname, object, repr_function
        # if return value of repr_function evals to False repr will not be added to log entry
        # eg: ('PokerGame', self, lambda game: game.id)
        # refs will be converted to weak refs, so we don't leak memory
        self._refs = []
        for ref in refs:
            self.addRef(*ref)

    def _log(self, level, message, *arg, **kw):
        refs = kw.get('refs', [])
        if 'refs' in kw:
            del kw['refs']
        #
        # calc ref string
        ref_string = "".join("<%s %s>" % (n, f(o)) for n, o, f in (self._refs + refs) if f(o) != None)

        #
        # pass to python logging
        kw.update({'extra':{'refs': ref_string}})
        self._logger.log(level, message, *arg, **kw)

    def addRef(self, name, obj, func):
        assert callable(func), "Function has to be callable"
        self._refs.append((name, obj, func))

    def getChild(self, name, refs=[]):
        return Logger(name, parent=self, refs=refs)

    # Logging functions
    
    def debug(self, *arg, **kw):
        """DEBUG: Info useful to developers for debugging the application, not useful during operations"""
        self._log(logging.DEBUG, *arg, **kw)

    def inform(self, *arg, **kw):
        """INFORMATIONAL: Normal operational messages - may be harvested for reporting, measuring throughput, etc - no action required"""
        self._log(logging.INFO, *arg, **kw)

    def warn(self, *arg, **kw):
        """WARNING: Warning messages - not an error, but indication that an error will occur if action is not taken, e.g. file system 85% full - each item must be resolved within a given time"""
        self._log(logging.WARNING, *arg, **kw)

    def error(self, *arg, **kw):
        """ERROR: Non-urgent failures - these should be relayed to developers or admins; each item must be resolved within a given time"""
        self._log(logging.ERROR, *arg, **kw)

    def crit(self, *arg, **kw):
        """CRITICAL: Should be corrected immediately, but indicates failure in a primary system - fix CRITICAL problems before ALERT - example is loss of primary ISP connection"""
        self._log(logging.CRITICAL, *arg, **kw)

# extended logging.Logger
class _LogRecord(logging.LogRecord):
    
    def __init__(self, *arg, **kw):
        self.refs = arg[-1].get('refs', '[]')
        logging.LogRecord.__init__(self, *arg[0:-1], **kw)

class _Logger(logging.getLoggerClass()):

    def makeRecord(self, *arg, **kw):
        return _LogRecord(*arg, **kw)

class SingleLineFormatter(logging.Formatter):

    def format(self, record):
        ret = []
        try:
            message = record.msg % record.args
        except:
            raise ValueError(str(record))
        record.args = tuple()
        for msg in message.split('\n'):
            record.msg = msg
            ret.append(logging.Formatter.format(self, record))
        return "\n".join(ret)

class TwistedHandler(logging.Handler):

    def __init__(self, log_publisher):
        logging.Handler.__init__(self)
        self._log_publisher = log_publisher

    def emit(self, record):
        for message in self.format(record).split('\n'):
            self._log_publisher.msg(message, system=record.name, syslogPriority=record.levelno)

logging.setLoggerClass(_Logger)
