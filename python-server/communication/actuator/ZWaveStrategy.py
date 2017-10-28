from typeguard import typechecked

from communication.ZWaveDevice import ZWaveDevice
from .BaseStrategy import BaseStrategy
from repository.ActuatorsRepository import ActuatorsRepository


class ZWaveStrategy(BaseStrategy):
    @typechecked()
    def __init__(self, actuators_repo: ActuatorsRepository, zwave_device: ZWaveDevice):
        self.__zwave_device = zwave_device
        self.__actuators_repo = actuators_repo

    def supports(self, actuator_name: str) -> bool:
        return self.__actuators_repo.get_actuators()[actuator_name].strategy == 'zwave-switch'

    def toggle(self, actuator_name: str, state: bool) -> bool:
        return self.__zwave_device.change_bistate_actuator(
            self.__actuators_repo.get_actuators()[actuator_name].send_to_device, state)