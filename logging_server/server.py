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

import logging
import logging.handlers
import socketserver
import threading
from typing import *

from .handlers import LogRecordStreamHandler


class LoggingServer(socketserver.ThreadingTCPServer):
    """The SocketServer which receive Logs."""

    allow_reuse_address = True
    daemon_threads = True

    def __init__(
        self,
        host="localhost",
        port=logging.handlers.DEFAULT_TCP_LOGGING_PORT,
        handler=LogRecordStreamHandler,
        logger_name: str = __name__,
    ):
        super().__init__((host, port), handler)
        self.timeout = 1
        self.logname = logger_name
        self.logger = logging.getLogger(logger_name)
        self.__shutdown = True
        self.server_thread: Optional[threading.Thread] = None

    def serve_until_stopped(self):
        import select

        while not self.__shutdown:
            rd, wr, ex = select.select([self.socket.fileno()], [], [], self.timeout)
            if rd:
                self.handle_request()

        self.logger.info("Logging Server stopped.")

    def start(self):
        """Starts serve_until_stopped roop as a daemon thread."""
        self.__shutdown = False
        self.server_thread = threading.Thread(target=self.serve_until_stopped, daemon=True)
        self.server_thread.start()
        self.logger.info("About starting Logging Server...")

    def shutdown(self):
        """Stops serve_until_stopped roop."""
        self.__shutdown = True
        self.logger.info("Shutdown Logging Server...")

    @property
    def is_shutdown(self) -> bool:
        return self.__shutdown

    def __enter__(self):
        """Starts server."""
        self.start()

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Shutdown server"""
        self.shutdown()
