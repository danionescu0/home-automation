from typeguard import typechecked
from .BaseStrategy import BaseStrategy

from tools.AsyncJobs import AsyncJobs

class GroupStrategy(BaseStrategy):
    @typechecked()
    def __init__(self, actuators_config: dict, job_controll: AsyncJobs):
        super(GroupStrategy, self).__init__(actuators_config)
        self.__job_controll = job_controll

    @typechecked()
    def supports(self, actuator_name: str) -> bool:
        return self.actuators_config[actuator_name]['strategy'] == 'group'

    @typechecked()
    def toggle(self, actuator_name: str, state: bool) -> bool:
        toggle_actuators = self.actuators_config[actuator_name]['actuators']
        future_state = self.actuators_config[actuator_name]['futureState']
        for actuator_name in toggle_actuators:
            self.__job_controll.change_actuator(actuator_name, future_state)

        return True