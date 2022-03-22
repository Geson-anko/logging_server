# Logging Server
multiprocessingによる並列処理中のロギング

# Installation
このリポジトリをクローンし、このディレクトリで次のコマンドを実行してインストールしてください。  
python=^3.9です。

```shell
pip install -e ./
```

# Usage
並列処理をする前にmain process でLoggingServerを建ててください。  
** 必ず `if __name__ == "__main__":`で保護してください **  

main.py
```python
from logging_server import LoggingServer
import logging

if __name__ == "__main__":
    ls = LoggingServer(
        host="localhost", 
        port=logging.handlers.DEFAULT_TCP_LOGGING_PORT
    )
    ls.start()

    # parallel processings ...

    ls.shutdown() # end of main process
```
ls.loggerはインスタンス時にはRootLoggerが割り当てられています。
標準出力は以下のように使用することができます。

```python
import sys
import logging
from logging_server import LoggingServer

if __name__ == "__main__":
    ls = LoggingServer(...)
    sh = logging.StreamHandler(sys.stdout)
    ls.logger.addHandler(sh)
    ls.start()
    ...
    ls.shutdown()
```

他のプロセスでは専用のロガークラスを使用します  

other_process.py
```python
from logging_server import SocketLogger
import logging

logger = SocketLogger(
    name=__name__,
    level=logging.NOTSET,
    host="localhost",
    port=logging.handlers.DEFAULT_TCP_LOGGING_PORT
)
logger.warning("warning")
```

このロガーは先ほど建てたLoggingServerクラスにログレコードを送信します。  
このロガークラスは```logging.Logger```クラスの不完全なラッパーです。  
```multiprocessing```による並列処理中ではpropagateがうまく機能しません。またプロセスの分岐後には```logging.getLogger``` をリセットしなければ正常に動作しないため、そういったチェックが入っています。


