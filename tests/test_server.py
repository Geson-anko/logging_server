from logging_server.server import LoggingServer
import logging
import sys
import time
ls = LoggingServer(port=8316)
def test_init():
    assert ls.is_shutdown == True
    assert ls.timeout == 1
    assert ls.logname == "logging_server.server"

def test_is_shutdown():
    ls.start()
    assert ls.is_shutdown == False

    ls.shutdown()
    assert ls.is_shutdown == True

def test_with_statement():
    with ls:
        assert ls.is_shutdown == False
    assert ls.is_shutdown == True