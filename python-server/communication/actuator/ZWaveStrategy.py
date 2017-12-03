from typeguard import typechecked

from communication.ZWaveDevice import ZWaveDevice
from .BaseStrategy import BaseStrategy
from repository.ActuatorsRepository import ActuatorsRepository
from model.Actuator import Actuator
from model.ActuatorProperties import ActuatorProperties


class ZWaveStrategy(BaseStrategy):
    @typechecked()
    def __init__(self, actuators_repo: ActuatorsRepository, zwave_device: ZWaveDevice):
        self.__zwave_device = zwave_device
        self.__actuators_repo = actuators_repo

    @typechecked()
    def supports(self, id: str) -> bool:
        return self.__actuators_repo.get_actuator(id).device_type == Actuator.DeviceType.ZWAVE.value

    @typechecked()
    def set_state(self, id: str, state) -> bool:
        actuator = self.__actuators_repo.get_actuator(id)
        send_to_device = actuator.properties.get(ActuatorProperties.SEND_TO_DEVICE)
        if actuator.type == Actuator.ActuatorType.SWITCH.value:
            return self.__zwave_device.change_switch(send_to_device, state)
        elif actuator.type == Actuator.ActuatorType.DIMMER.value:
            return self.__zwave_device.change_dimmer(send_to_device, self.__remap_with_max_value(actuator, int(state)))

    @typechecked()
    def __remap_with_max_value(self, actuator: Actuator, value: int) -> int:
        max_value_for_actuator = actuator.properties.get(ActuatorProperties.MAX_VALUE)

        return int(value * max_value_for_actuator / Actuator.ActuatorType.MAX_DIMMER_VALUE.value)