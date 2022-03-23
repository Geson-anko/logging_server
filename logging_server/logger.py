"""
Logger class for mutiprocessing logging.

Usage:
    from logging_server import SocketLogger
    logger = SocketLogger(__name__)
    logger.setLevel(0)
    logger.debug("debug")
    logger.info("info")
    logger.warning("warning")
    logger.error("error")
    logger.exception("exception")


このロガークラスはlogging.Loggerクラスを継承せずにラップしているため、
純粋なロガークラスの様に振る舞わないことに注意してください。
ロギングに必要なメソッドのみを提供します。
また任意のハンドラーを追加しても正常に機能しないことがあります。
"""
import os
import logging
import logging.handlers

def _check_pid(func):
    def check(self,*args, **kwds):
        pid = os.getpid()
        if self._pid != pid:
            self._pid = pid
            self.reset_logger()
        func(self,*args, **kwds)
    return check
class SocketLogger:
    _pid:int = None
    __logger:logging.Logger = None
    def __init__(
        self, name:str, level:int=logging.NOTSET, host="localhost",
        port:int=logging.handlers.DEFAULT_TCP_LOGGING_PORT,
    ) -> None:
        self._pid = os.getpid()
        self.name = name
        self.level = level
        self.host = host
        self.port = port
        self.set_logger()

    @property
    def logger(self):
        return self.__logger

    def setLevel(self, level:int) -> None:
        self.logger.setLevel(level)

    def set_logger(self):
        """set logger class, name, level and socket handler."""
        self.__logger = logging.Logger(self.name)
        self.__logger.setLevel(self.level)
        socket_handler = logging.handlers.SocketHandler(self.host, self.port)
        socket_handler.setLevel(logging.NOTSET)
        self.__logger.addHandler(socket_handler)
        self.__logger.propagate=False # Because another logger is propagating in server process.

    def remove_handlers(self):
        """remove handlers of logger."""
        for hdlr in self.__logger.handlers:
            self.__logger.removeHandler(hdlr)

    def reset_logger(self):
        """reset logger class"""
        self.remove_handlers()
        self.set_logger()

    @_check_pid
    def debug(self,*args, **kwds) -> None: self.logger.debug(*args, **kwds)
    @_check_pid
    def info(self,*args, **kwds) -> None: self.logger.info(*args, **kwds)
    @_check_pid
    def warn(self,*args, **kwds) -> None: self.logger.warn(*args, **kwds)
    @_check_pid
    def warning(self,*args, **kwds) -> None: self.logger.warning(*args, **kwds)
    @_check_pid
    def error(self,*args, **kwds) -> None: self.logger.error(*args, **kwds)
    @_check_pid
    def critical(self,*args, **kwds) -> None: self.logger.critical(*args, **kwds)
    @_check_pid
    def exception(self,*args, **kwds) -> None: self.logger.exception(*args, **kwds)
    @_check_pid
    def log(self, *args,**kwds) -> None: self.logger.log(*args,**kwds)



