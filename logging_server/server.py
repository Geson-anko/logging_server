from .handlers import LogRecordStreamHandler
import socketserver
import logging
import logging.handlers
from dataclasses import dataclass
import threading
@dataclass
class Shutdown:
    value:bool = False
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
        self.__shutdown = Shutdown(False)
        self.server_thread:threading.Thread = None

    def serve_until_stopped(self):
        import select
        abort = 0
        while not abort and not self.__shutdown.value:
            rd, wr, ex = select.select([self.socket.fileno()], [], [], self.timeout)
            if rd:
                self.handle_request()
            abort = self.abort

    def start(self):
        self.server_thread = threading.Thread(target=self.serve_until_stopped)
        self.logger.info("About starting LoggingServer...")

    def shutdown(self,timeout:float=0.0):
        self.__shutdown.value = True
        self.server_thread.join(timeout)
        self.logger.info("Shutdown Logging Server.")
        



        