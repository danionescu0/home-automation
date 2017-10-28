import abc


class DeviceLifetimeCycles(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def connect(self):
        pass

    @abc.abstractmethod
    def disconnect(self) -> None:
        pass