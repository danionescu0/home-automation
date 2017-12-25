import abc

from typeguard import typechecked

from model.configuration.BaseConfig import BaseConfig


class HomeDefenceCfg(BaseConfig, metaclass=abc.ABCMeta):
    @typechecked()
    def __init__(self, alarm_lock_seconds: int, burgler_lights_switches: list, burgler_time_between_actions: int) -> None:
        self.alarm_lock_seconds = alarm_lock_seconds
        self.burgler_lights_switches = burgler_lights_switches
        self.burgler_time_between_actions = burgler_time_between_actions
        super(HomeDefenceCfg, self).__init__()

    @typechecked()
    def main_description(self) -> str:
        return 'Home defence'

    @typechecked()
    def properties_description(self) -> dict:
        return {
            'alarm_lock_seconds' : 'Number of seconds between two alarm notifications',
            'burgler_lights_switches' : 'Light switches to toggle ex: '
                                        '[\'livingLight\', \'kitchenLight\', \'holwayLight\']',
            'burgler_time_between_actions': "Number of seconds between light toggle"
        }