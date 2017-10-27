from typeguard import typechecked

from communication.ZWaveDevice import ZWaveDevice
from .BaseStrategy import BaseStrategy


class ZWaveStrategy(BaseStrategy):
    @typechecked()
    def __init__(self, actuators_config: dict, zwave_device: ZWaveDevice):
        super(ZWaveStrategy, self).__init__(actuators_config)
        self.__zwave_device = zwave_device

    def toggle(self, actuator_name: str, state: bool) -> bool:
        return self.__zwave_device.change_bistate_actuator(
            self.actuators_config[actuator_name]['send_to_device'], state)

    def supports(self, actuator_name: str) -> bool:
        return self.actuators_config[actuator_name]['strategy'] == 'zwave-switch'