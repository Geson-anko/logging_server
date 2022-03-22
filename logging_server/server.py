from .handlers import LogRecordStreamHandler
import socketserver
import logging
import logging.handlers
from dataclasses import dataclass
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
    
    def serve_until_stopped(self,shutdown):
        import select
        abort = 0
        while not abort and not shutdown.value:
            rd, wr, ex = select.select([self.socket.fileno()], [], [], self.timeout)
            if rd:
                self.handle_request()
            abort = self.abort