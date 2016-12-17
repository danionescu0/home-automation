import logging
import logging.handlers

class LoggingConfig():
    def __init__(self, filename, max_bytes):
        self.__filename = filename
        self.__max_bytes = max_bytes

    def get_logger(self):
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
        self.__root_logger.setLevel(logging.DEBUG)
        for h in handlers:
            h.setFormatter(formatter)
            h.setLevel(logging.DEBUG)
            self.__root_logger.addHandler(h)

        return self.__root_logger

    def set_error_hadler(self, type, value, tb):
        self.__root_logger.exception("Uncaught exception: {0}".format(str(value)))