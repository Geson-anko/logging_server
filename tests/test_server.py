from logging_server.server import LoggingServer
import logging
import sys
import time
ls = LoggingServer(port=8316)
def test_start():
    global ls
    sh = logging.StreamHandler(sys.stdout)
    ls.logger.addHandler(sh)
    ls.logger.setLevel(0)
    ls.start()
    time.sleep(0.5)
    ls.shutdown()


def test_delete_shutdown():
    global ls
    ls.start()
    time.sleep(0.5)
    del ls

def test_auto_shutdown():
    ls = LoggingServer(port=12345)
    ls.start()
    time.sleep(0.5)

