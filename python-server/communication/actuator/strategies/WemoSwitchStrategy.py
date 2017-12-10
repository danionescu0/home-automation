from typeguard import typechecked

from communication.WemoSwitch import WemoSwitch
from communication.actuator.strategies.BaseStrategy import BaseStrategy
from model.Actuator import Actuator
from model.ActuatorProperties import ActuatorProperties


class WemoSwitchStrategy(BaseStrategy):
    @typechecked()
    def __init__(self, wemo_switch: WemoSwitch):
        self.__wemo_switch = wemo_switch

    @typechecked()
    def supports(self, actuator: Actuator) -> bool:
        return actuator.device_type == Actuator.DeviceType.WEMO.value \
               and actuator.type == Actuator.ActuatorType.SWITCH.value

    @typechecked()
    def set_state(self, actuator: Actuator, state) -> bool:
        return self.__wemo_switch.change_state(
            actuator.properties.get(ActuatorProperties.SEND_TO_DEVICE), state
        )