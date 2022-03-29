from logging_server.logger import SocketLogger
from logging_server.server import LoggingServer
import logging
import sys

msg = """\033[31mYou must see below message after test.\033[0m
About starting LoggingServer...
start test logging
debug
info
warning
error
critical

Traceback (most recent call last):
  File "../logging_server/test_logger.py", line 17, in test_logging
    raise Exception
Exception
\033[31mYou must see above message after test.\033[0m
"""

def test_logging():
    print(msg)
    print("start test logging")
    logger = SocketLogger("test_logging")
    logger.debug("debug")
    logger.info("info")
    logger.warning("warning")
    logger.error("error")
    logger.critical("critical")
    try:
        raise Exception
    except Exception as e:
        pass
        logger.exception(e)


if __name__ == "__main__":

    ls = LoggingServer()
    sh = logging.StreamHandler(sys.stdout)
    sh.setLevel(0)
    ls.logger.addHandler(sh)
    ls.logger.setLevel(0)
    ls.start()
    test_logging()
