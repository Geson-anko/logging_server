"""
Logger class for mutiprocessing logging.

Usage:
    from logging_server import SocketLogger
    logger = SocketLogger(__name__)
    logger.setLevel(0)
    logger.debug("debug")
    logger.info("info")
    logger.warning("warning")
    logger.error("error")
    logger.exception("exception")


このロガークラスはlogging.Loggerクラスを継承せずにラップしているため、
純粋なロガークラスの様に振る舞わないことに注意してください。
ロギングに必要なメソッドのみを提供します。
また任意のハンドラーを追加しても正常に機能しないことがあります。
"""