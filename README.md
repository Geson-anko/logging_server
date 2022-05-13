# Logging Server
Logging tool for python multiprocessing.
# Installation
Please run a following command.
```shell
pip install git+https://github.com/Geson-anko/logging_server.git@main
```

Or, clone this repository and run a following command.

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

- with statement
```py
with LoggingServer(): # calling start()
    ...
# calling shutdown()
```

- Socket Logger  
It is an incomplete `logging.Logger` wrapper that does not inherit.
SocketLogger provides some methods to send logs to server.  
The logging methods (such as `logger.debug`) are decorated by `_pid_checker`, because `multiprocessing` causes the logger to be dereferenced and must be reset. So This logger calls `reset_logger` if the pid is changed.


```py
# host and port are the same as server.
logger = SocketLogger("SocketLogger",host="localhost",port=9999)
logger.debug("debug")
logger.info("info")
logger.warning("warning")
logger.error("error")
logger.critical("critical")
```

# Logging Structure
                     ┌───────────┐
                     │Root Logger│
                     └───────────┘
                           ▲
                           │
                           │
                       Propagate
                           │
        ┌──────────────────┴──────────────────┐
        │Logging Server (Threading TCP Server)│
        └─────────────────────────────────────┘
           ▲               ▲               ▲
           │               │               │
           │               │               │
         Send            Send            Send
           │               │               │
    ┌──────┴──────┐ ┌──────┴──────┐ ┌──────┴──────┐
    │Socket Logger│ │Socket Logger│ │Socket Logger│
    └─────────────┘ └─────────────┘ └─────────────┘