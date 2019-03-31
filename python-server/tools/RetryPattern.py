import time
from logging import RootLogger

from typeguard import typechecked


class RetryPattern:
    @typechecked()
    def __init__(self, logger: RootLogger):
        self.__logger = logger

    @typechecked
    def run(self, function, times: int, starting_delay: float=0.2, multiplier: float=2):
        for i in range(1, times):
            try:
                return function()
            except Exception as e:
                self.__logger.error('Error trying to call method {0}, error is: {1}, retrying'
                                    .format(function.__name__, repr(e)))
            time.sleep(starting_delay)
            starting_delay *= multiplier