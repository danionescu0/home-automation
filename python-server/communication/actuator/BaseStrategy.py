import abc

class BaseStrategy:
    __metaclass__ = abc.ABCMeta

    def __init__(self, actuators_config):
        self.actuators_config = actuators_config

    @abc.abstractmethod
    def supports(self, actuator_name):
        pass

    @abc.abstractmethod
    def toggle(self, actuator_name, state):
        pass