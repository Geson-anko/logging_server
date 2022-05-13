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
    ls = LoggingServer(port=12345)
    ls.start()
    time.sleep(0.5)
    del ls

def test_auto_shutdown():
    ls.start()
    time.sleep(0.5)

def test_set_logger_modifier():
    global ls
    def modifier(logger):
        return logger

    ls.set_logger_modifier(modifier)
    assert ls.logger_modifier == modifier
    

def test_is_shutdown():
    ls.start()
    assert ls.is_shutdown == False

    ls.shutdown()
    assert ls.is_shutdown == True

