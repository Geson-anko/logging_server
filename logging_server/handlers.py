import socketserver
import struct
import logging
import pickle
from typing import *

class LogRecordStreamHandler(socketserver.StreamRequestHandler):
    """Read the LogRecord binary and process it."""

    # logger saver
    loggers = dict()

    def handle(self):
        """make the LogRecord object from binary and process it."""
        while True:
            chunk = self.connection.recv(4)
            if len(chunk) < 4:
                break
            slen = struct.unpack(">L",chunk)[0]
            chunk = self.connection.recv(slen)
            while len(chunk) < slen:
                chunk = chunk + self.connection.recv(slen - len(chunk))
            obj = self.unPickle(chunk)
            record = logging.makeLogRecord(obj)
            self.handleLogRecord(record)

    def unPickle(self, data:bytes) -> Any:
        return pickle.loads(data)
    
    def handleLogRecord(self, record:logging.LogRecord) -> None:
        """ process the LogRecord object."""
        if self.server.logname is not None:
            name = self.server.logname
        else:
            name = record.name

        # if already exists the logger, use it.
        if name in self.loggers:
            logger = self.loggers[name]
        else:
            logger = logging.getLogger(name)
            logger.propagate = True
            
            logger = self.modify_logger(logger)

            self.loggers[name] = logger
        logger.handle(record)

    def modify_logger(self,logger:logging.Logger) -> logging.Logger:
        """modify logger if server has logger modifier."""
        if hasattr(self.server,"logger_modifier"):
            _logger = self.server.logger_modifier(logger)
            if _logger: # if logger modifier does not return logger.
                logger = _logger
        return logger