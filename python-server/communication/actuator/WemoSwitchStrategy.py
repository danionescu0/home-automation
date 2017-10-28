from typeguard import typechecked

from .BaseStrategy import BaseStrategy
from communication.WemoSwitch import WemoSwitch
from repository.ActuatorsRepository import ActuatorsRepository


class WemoSwitchStrategy(BaseStrategy):
    @typechecked()
    def __init__(self, actuators_repo: ActuatorsRepository, wemo_switch: WemoSwitch):
        self.__wemo_switch = wemo_switch
        self.__actuators_repo = actuators_repo

    @typechecked()
    def supports(self, actuator_name: str) -> bool:
        return self.__actuators_repo.get_actuators()[actuator_name].strategy == 'wemo-switch'

    @typechecked()
    def toggle(self, actuator_name: str, state) -> bool:
        return self.__wemo_switch.change_state(
            self.__actuators_repo.get_actuators()[actuator_name].send_to_device, state)