from logging_server import LoggingServer,SocketLogger
import multiprocessing as mp
from logging import INFO
import sys
import logging
import time

#root = logging.getLogger()
#sh = logging.StreamHandler(sys.stdout)
#root.addHandler(sh)
#root.setLevel(0)

NUM_PROCESSES = 3
def process_func(num:int) -> None:
    logger = SocketLogger(f"process{num}")
    logger.info(f"logged from process{num}")

def _mp_logging():
    ls = LoggingServer() # save multiple calling.
    ls.start()
    
    with mp.Pool() as p:
        nums = list(range(NUM_PROCESSES))
        p.map(process_func, nums)
    time.sleep(0.01)


def test_mp_logging(caplog):
    caplog.set_level(0)
    _mp_logging()

    rec_tup = caplog.record_tuples
    assert ('process0', INFO, 'logged from process0') in rec_tup
    assert ('process1', INFO, 'logged from process1') in rec_tup
    assert ('process2', INFO, 'logged from process2') in rec_tup


