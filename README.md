# Logging Server
Logging tool for python multiprocessing.
# Installation
Please clone this repository and run a following command.

```shell
pip install -e ./
```

# Examples
### Good
```py
from logging_server import LoggingServer, SocketLogger
import logging, sys

def process(process_name:str) -> None:
    logger = SocketLogger(process_name) # <- using SocketLogger
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
```

### Bad
```py
from logging_server import LoggingServer, SocketLogger
import logging, sys

def process(process_name:str) -> None:
    logger = logging.getLogger(process_name) # <- using default logger.
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
```

# Usage
- Import server and logger
```py
from logging_server import LoggingServer, SocketLogger
```

- Build server
The logging server must be protected with `if __name__ == "__main__":`
```py
if __name__ == "__main__":
    ls = LoggingServer(host="localhost", port=9999)
    ls.start() # Server runs in daemon thread. 
```

- Shutdown server    
You don't need to call this method at the end of the script because logging server runs in daemon thread.
```py
...
ls.shutdown()
...
```

- Socket Logger  
It is an incomplete `logging.Logger` wrapper that does not inherit.  
SocketLogger provides some methods to send logs to server.
```py
# host and port are the same as server.
logger = SocketLogger("SocketLogger",host="localhost",port=9999)
logger.debug("debug")
logger.info("info")
logger.warning("warning")
logger.error("error")
logger.critical("critical")
```

- Logger modifier
The Logging Server gets the logger in the thread when the Log is sent. (In fact, RogRecordStreamHandler does it.)
Then, a function can be set up to make modifications to the logger.

```py
import logging

def modifier(logger:logging.Logger) -> logging.Logger:
    fh = logging.FileHandler(logger.name+".log")
    logger.addHandler(fh)
    return logger

if __name__ == "__main__":
    ls = LoggingServer()
    ls.set_logger_modifier(modifier)
    ls.start()
```






