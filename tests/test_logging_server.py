from logging_server import __version__
from logging_server import LoggingServer, SocketLogger
import logging, sys
import time

#ls = LoggingServer()
#ls.logger.setLevel(0)
#sh = logging.StreamHandler(sys.stdout)
#ls.logger.addHandler(sh)
#ls.start()

def test_version():
    assert __version__ == '0.1.0'

    
