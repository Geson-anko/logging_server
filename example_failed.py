from logging_server import LoggingServer, SocketLogger
import logging, sys

def process(process_name:str) -> None:
    logger = logging.getLogger(process_name)
    logger.info(f"Start {process_name}")
    # ... some process ...

if __name__ == "__main__":
    import multiprocessing as mp
    
    logger = logging.getLogger() # root logger
    logger.addHandler(logging.StreamHandler(sys.stdout)) # output to console.
    logger.setLevel(logging.NOTSET) # lowest logger level

    ls = LoggingServer()
    ls.start()
    print("start processes.")
    for i in range(10):
        p = mp.Process(target=process, args=(f"process {i}",))
        p.start()
