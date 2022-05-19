from logging_server.logger import SocketLogger
from logging_server.server import LoggingServer
import multiprocessing as mp
import sys
import logging
import time

PORT = 10005
outer_logger = SocketLogger("outer_logger",port=PORT)

def process_func(num:int) -> None:
    outer_logger.info("Logging after process")
    logger = SocketLogger(f"process{num}",port=PORT)
    logger.info(f"logged from process{num}")

def test_multiprocessing_logging():
    ls = LoggingServer(port=PORT)
    sh = logging.StreamHandler(sys.stdout)
    sh.setLevel(0)
    logger = logging.getLogger()
    logger.addHandler(sh)
    logger.setLevel(0)
    ls.start()
    outer_logger.info("start test.")
    time.sleep(0.5)
    with mp.Pool() as p:
        nums = [*range(3)]
        out = p.map(process_func, nums)
    time.sleep(2)
    outer_logger.info("end test.")
    ls.shutdown()
        

if __name__ == "__main__":
    mp.freeze_support()
    test_multiprocessing_logging()