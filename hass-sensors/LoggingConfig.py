import logging
import logging.handlers
from logging import RootLogger
import traceback


class LoggingConfig:
    def __init__(self):
        self.__filename = 'log.txt'
        self.__max_bytes = 20000000

    def get_logger(self) -> RootLogger:
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
        self.__root_logger.setLevel(logging.INFO)
        for h in handlers:
            h.setFormatter(formatter)
            h.setLevel(logging.INFO)
            self.__root_logger.addHandler(h)
        return self.__root_logger

    def set_error_hadler(self, type, value, tb):
        self.__root_logger.exception("Uncaught exception: {0}".format(str(value)))
        self.__root_logger.exception("Uncaught exception: {0}".format(traceback.format_tb(tb)))