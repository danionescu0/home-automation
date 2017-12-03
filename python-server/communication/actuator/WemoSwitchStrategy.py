from typeguard import typechecked

from .BaseStrategy import BaseStrategy
from communication.WemoSwitch import WemoSwitch
from repository.ActuatorsRepository import ActuatorsRepository
from model.Actuator import Actuator
from model.ActuatorProperties import ActuatorProperties


class WemoSwitchStrategy(BaseStrategy):
    @typechecked()
    def __init__(self, actuators_repo: ActuatorsRepository, wemo_switch: WemoSwitch):
        self.__wemo_switch = wemo_switch
        self.__actuators_repo = actuators_repo

    @typechecked()
    def supports(self, id: str) -> bool:
        actuator = self.__actuators_repo.get_actuator(id)

        return actuator.device_type == Actuator.DeviceType.WEMO.value \
               and actuator.type == Actuator.ActuatorType.SWITCH.value

    @typechecked()
    def set_state(self, id: str, state) -> bool:
        return self.__wemo_switch.change_state(
            self.__actuators_repo.get_actuators()[id].properties.get(ActuatorProperties.SEND_TO_DEVICE), state
        )