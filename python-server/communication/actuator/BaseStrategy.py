import abc

class BaseStrategy:
    __metaclass__ = abc.ABCMeta

    def __init__(self, actuators_config):
        self.actuators_config = actuators_config
        self.__encriptor = None

    @abc.abstractmethod
    def supports(self, actuator_name):
        pass

    def set_encription(self, encriptor):
        self.__encriptor = encriptor
        return self

    def get_encriptor(self):
        return self.__encriptor

    @abc.abstractmethod
    def toggle(self, actuator_name, state):
        pass