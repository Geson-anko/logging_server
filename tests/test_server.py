from logging_server.server import LoggingServer
import logging
import sys
import time
ls = LoggingServer(port=8316)
def test_start():
    ls.start()
    time.sleep(0.01)
    ls.shutdown()

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

def test_with_statement():
    with ls:
        assert ls.is_shutdown == False
    assert ls.is_shutdown == True