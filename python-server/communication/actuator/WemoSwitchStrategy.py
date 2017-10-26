from typeguard import typechecked


from .BaseStrategy import BaseStrategy
from communication.WemoSwitch import WemoSwitch

# todo replace actuators_config with actuators_repo
class WemoSwitchStrategy(BaseStrategy):
    @typechecked()
    def __init__(self, actuators_config: dict, wemo_switch: WemoSwitch):
        super(WemoSwitchStrategy, self).__init__(actuators_config)
        self.__wemo_switch = wemo_switch

    @typechecked()
    def supports(self, actuator_name: str) -> bool:
        return self.actuators_config[actuator_name]['strategy'] == 'wemo-switch'

    @typechecked()
    def toggle(self, actuator_name: str, state) -> bool:
        return self.__wemo_switch.change_state(self.actuators_config[actuator_name]['send_to_device'], state)