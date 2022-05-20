import logging
import pickle
import socketserver
import struct
from typing import *


class LogRecordStreamHandler(socketserver.StreamRequestHandler):
    """Read the LogRecord binary and process it."""

    def handle(self):
        """make the LogRecord object from binary and process it."""
        while True:
            chunk = self.connection.recv(4)
            if len(chunk) < 4:
                break
            slen = struct.unpack(">L", chunk)[0]
            chunk = self.connection.recv(slen)
            while len(chunk) < slen:
                chunk = chunk + self.connection.recv(slen - len(chunk))
            obj = self.unPickle(chunk)
            record = logging.makeLogRecord(obj)
            self.handleLogRecord(record)

    def unPickle(self, data: bytes) -> Any:
        return pickle.loads(data)

    def handleLogRecord(self, record: logging.LogRecord) -> None:
        """process the LogRecord object."""
        logger = logging.getLogger()
        logger.handle(record)
