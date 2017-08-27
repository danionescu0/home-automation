from typeguard import typechecked

from .BaseStrategy import BaseStrategy
from communication.CommunicatorRegistry import CommunicatorRegistry


class WemoSwitchStrategy(BaseStrategy):
    @typechecked()
    def __init__(self, actuators_config: dict, communication_registry: CommunicatorRegistry):
        super(WemoSwitchStrategy, self).__init__(actuators_config)
        self.__communication_registry = communication_registry

    @typechecked()
    def supports(self, actuator_name: str) -> bool:
        return self.actuators_config[actuator_name]['strategy'] == 'wemo-switch'

    @typechecked()
    def toggle(self, actuator_name: str, state: bool) -> bool:
        return self.__communication_registry.get_communicator('wemo_switch').\
            send(self.actuators_config[actuator_name]['send_to_device'], str(state).encode())