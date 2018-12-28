import abc


class BaseProcessor(metaclass=abc.ABCMeta):
    def process(self, dataframe):
        pass
