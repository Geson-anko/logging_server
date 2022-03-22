from logging_server.server import LoggingServer
import logging
import sys
import time

def test_start():
    ls = LoggingServer()
    sh = logging.StreamHandler(sys.stdout)
    ls.logger.addHandler(sh)
    ls.logger.setLevel(0)
    ls.start()
    time.sleep(0.5)
    ls.shutdown()
    
