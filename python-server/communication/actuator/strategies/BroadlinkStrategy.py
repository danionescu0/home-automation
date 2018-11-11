from typeguard import typechecked

from communication.BroadlinkDevice import BroadlinkDevice
from communication.actuator.strategies.BaseStrategy import BaseStrategy
from model.Actuator import Actuator
from model.ActuatorProperties import ActuatorProperties


class BroadlinkStrategy(BaseStrategy):
    @typechecked()
    def __init__(self, broadlink_device: BroadlinkDevice):
        self.__broadlink_device = broadlink_device

    @typechecked()
    def supports(self, actuator: Actuator) -> bool:
        return actuator.device_type == Actuator.DeviceType.BROADLINK.value \
               and actuator.type == Actuator.ActuatorType.PUSHBUTTON.value

    @typechecked()
    def set_state(self, actuator: Actuator, state) -> bool:
        command = actuator.properties.get(ActuatorProperties.COMMAND)

        return self.__broadlink_device.send(command)