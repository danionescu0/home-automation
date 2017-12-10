import logging
import logging.handlers
from logging import RootLogger
import traceback

from typeguard import typechecked


class LoggingConfig():
    @typechecked()
    def __init__(self, filename: str, max_bytes: int):
        self.__filename = filename
        self.__max_bytes = max_bytes

    @typechecked()
    def get_logger(self, level : int) -> RootLogger:
        formatter = logging.Formatter(fmt='%(levelname)s (%(threadName)-10s) :%(name)s: %(message)s '
                                  '(%(asctime)s; %(filename)s:%(lineno)d)',
                              datefmt="%Y-%m-%d %H:%M:%S")
        handlers = [
            logging.handlers.RotatingFileHandler(self.__filename,
                                                 encoding='utf8',
                                                 maxBytes=self.__max_bytes,
                                                 backupCount=3),
            logging.StreamHandler()
        ]
        self.__root_logger = logging.getLogger()
        self.__root_logger.setLevel(level)
        for handler in handlers:
            handler.setFormatter(formatter)
            handler.setLevel(level)
            self.__root_logger.addHandler(handler)

        return self.__root_logger

    def set_error_hadler(self, type, value, tb):
        self.__root_logger.exception("Uncaught exception: {0}".format(str(value)))
        self.__root_logger.exception("Uncaught exception: {0}".format(traceback.format_tb(tb)))