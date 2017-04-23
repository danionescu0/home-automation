from .BaseStrategy import BaseStrategy

class WemoSwitchStrategy(BaseStrategy):
    def __init__(self, actuators_config, communication_registry):
        super(WemoSwitchStrategy, self).__init__(actuators_config)
        self.__communication_registry = communication_registry

    def supports(self, actuator_name):
        return self.actuators_config[actuator_name]['strategy'] == 'wemo-switch'

    def toggle(self, actuator_name, state):
        return self.__communication_registry.get_communicator('wemo_switch').\
            send(self.actuators_config[actuator_name]['send_to_device'], state)