from logging_server.logger import SocketLogger
from logging_server.server import LoggingServer
import logging
import sys
import time
import logging
import os

PORT = 10001
ls = LoggingServer(port=PORT)
ls.start()

def test__init__():
    logger = SocketLogger("socketlogger", logging.ERROR, "127.0.0.1", 10001)
    
    assert logger._pid == os.getpid()
    assert logger.name == "socketlogger"
    assert logger.level == logging.ERROR
    assert logger.host == "127.0.0.1"
    assert logger.port == 10001

def test__reduce__():
    logger = SocketLogger("__reduce__")
    logger.__reduce__()
    assert logger.logger is None
    

def _test_logging():
    #print(msg)
    #print("start test logging")
    logger = SocketLogger("test_logging",port=PORT)
    logger.debug("debug")
    logger.info("info")
    logger.warning("warning")
    logger.error("error")
    logger.critical("critical")
    try:
        raise Exception
    except Exception as e:
        logger.exception(e)

def test_logging(caplog):
    caplog.set_level(0)
    _test_logging()
    time.sleep(0.01)
    d,i,w,e,c,exc = caplog.records
    assert d.levelname == "DEBUG"
    assert d.msg == "debug"
    assert i.levelname == "INFO"
    assert i.msg == "info"
    assert w.levelname == "WARNING"
    assert w.msg == "warning"
    assert e.levelname == "ERROR"
    assert e.msg == "error"
    assert c.levelname == "CRITICAL"
    assert c.msg == "critical"
    assert exc.levelname == "ERROR"
    assert exc.msg == ""


if __name__ == "__main__":

    ls = LoggingServer()
    sh = logging.StreamHandler(sys.stdout)
    sh.setLevel(0)
    ls.logger.addHandler(sh)
    ls.logger.setLevel(0)
    ls.start()
    test_logging()
