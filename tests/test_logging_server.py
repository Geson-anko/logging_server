from logging_server import __version__
from logging_server import LoggingServer, SocketLogger
import logging, sys

ls = LoggingServer()
ls.logger.setLevel(0)
sh = logging.StreamHandler(sys.stdout)
ls.logger.addHandler(sh)
ls.start()

def test_version():
    assert __version__ == '0.1.0'

def test_logger_modifier():
    def modifier(logger:logging.Logger) -> logging.Logger:
        sh = logging.StreamHandler(sys.stdout)
        fmt = logging.Formatter("|||%(name)s|%(message)s|||")
        sh.setFormatter(fmt)
        logger.addHandler(sh)
        logger.setLevel(0)
    
        return logger
    
    ls.set_logger_modifier(modifier)

    logger = SocketLogger("test_logger_modifier")
    logger.info("log from test_logger_modifier.")

    
