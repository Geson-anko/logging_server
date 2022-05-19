import multiprocessing as mp
from logging_server import LoggingServer, SocketLogger
import sys, logging
import time
from logging import INFO

root = logging.getLogger()
sh = logging.StreamHandler(sys.stdout)
root.addHandler(sh)
root.setLevel(0)

PORT = 10004
NUM_PROCESSES = 3

class Log:
    def __init__(self, num:int) -> None:
        self.name = f"Log{num}"
        self.logger = SocketLogger(self.name, port=PORT)
    def __call__(self) -> None:
        self.logger.info(f"logged from {self.name}")
        
def pickled_logging():
    ls = LoggingServer(port=PORT)
    ls.start()
    
    for i in range(NUM_PROCESSES):
        p = mp.Process(target=Log(i),)
        p.start()
    time.sleep(2)

def test_process_logging(caplog):
    pickled_logging()
    rec_tup = caplog.record_tuples
    assert ('Log0', INFO, 'logged from Log0') in rec_tup
    assert ('Log1', INFO, 'logged from Log1') in rec_tup
    assert ('Log2', INFO, 'logged from Log2') in rec_tup