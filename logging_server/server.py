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

"""

from .handlers import LogRecordStreamHandler
import socketserver
import logging
import logging.handlers
import threading

class LoggingServer(socketserver.ThreadingTCPServer):
    """The SocketServer which receive Logs."""

    allow_reuse_address = True

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
        self.logger.info("About starting LoggingServer...")

    def shutdown(self,timeout:float=0.0):
        self.__shutdown = True
        self.server_thread.join(timeout)
        self.logger.info("Shutdown Logging Server.")

    def __del__(self):
        self.shutdown()
        


        