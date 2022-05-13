from logging_server import __version__
from logging_server import LoggingServer, SocketLogger
import logging, sys
import time

ls = LoggingServer()
ls.logger.setLevel(0)
sh = logging.StreamHandler(sys.stdout)
ls.logger.addHandler(sh)
ls.start()

def test_version():
    assert __version__ == '0.1.0'

def _output_logger_modifier():
    def modifier(logger:logging.Logger) -> logging.Logger:
        sh = logging.StreamHandler(sys.stdout)
        fmt = logging.Formatter("test_logging_modifier() -> %(name)s|%(message)s")
        sh.setFormatter(fmt)
        logger.addHandler(sh)
        logger.setLevel(0)
    
        return logger
    
    ls.set_logger_modifier(modifier)

    logger = SocketLogger("test_logger_modifier")
    logger.info("log from test_logger_modifier.")

def test_logger_modifier(capfd):
    _output_logger_modifier()
    time.sleep(0.01)
    out,err = capfd.readouterr()
    assert out == "test_logging_modifier() -> test_logger_modifier|log from test_logger_modifier.\n"
    assert err == ""

    
