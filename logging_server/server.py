"""Logging Server for multiprocessing logging managements.
Basic usage:
    >>> import logging, sys
    >>> ls = LoggingServer()
    >>> sh = logging.StreamHandler(sys.stdout)
    >>> ls.logger.addHandler(sh)
    >>> ls.start() # run server in other thread.
    >>> # your process
    ... 
    >>> # end process
    >>> # Server thread is deamon, so you don't need call `ls.shutdown()`
    >>> ls.shutdown() # If you need. `del ls` is same.

    You can use any server address
    >>> ls = LoggingServer(host="127.0.0.1", port=9999)
"""

from .handlers import LogRecordStreamHandler
import socketserver
import logging
import logging.handlers
import threading
from typing import *
class LoggingServer(socketserver.ThreadingTCPServer):
    """The SocketServer which receive Logs."""

    allow_reuse_address = True
    logger_modifier:Callable = lambda x:x

    def __init__(self,host='localhost',port=logging.handlers.DEFAULT_TCP_LOGGING_PORT, 
                handler=LogRecordStreamHandler):
        super().__init__((host, port), handler)
        self.abort = 0
        self.timeout = 1
        self.logname = None
        self.logger = logging.getLogger()
        self.__shutdown = False
        self.server_thread:threading.Thread = None

    def serve_until_stopped(self):
        import select
        abort = 0
        while not abort and not self.__shutdown:
            rd, wr, ex = select.select([self.socket.fileno()], [], [], self.timeout)
            if rd:
                self.handle_request()
            abort = self.abort

    def start(self):
        self.__shutdown= False
        self.server_thread = threading.Thread(target=self.serve_until_stopped,daemon=True)
        self.server_thread.start()
        self.logger.info("About starting Logging Server...")

    def shutdown(self,timeout:float=0.0):
        self.__shutdown = True
        self.server_thread.join(timeout)
        self.logger.info("Shutdown Logging Server.")

    def __del__(self):
        self.shutdown()
        
    def set_logger_modifier(self, func:Callable) -> None:
        """set func to add handlers or filters to specified logger.
        The func must have a argument for logger, and returns logger class.
        """
        if callable(func):
            self.logger_modifier = func
        else:
            raise ValueError("logger modifier must be callable! input: {}".format(func))
        


        