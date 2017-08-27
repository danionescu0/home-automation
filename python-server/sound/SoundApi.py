import abc

from typeguard import typechecked


class SoundApi(metaclass=abc.ABCMeta):
    @typechecked()
    @abc.abstractmethod
    def say(self, text: str, nr_times = 1) -> bool:
        pass