from typeguard import typechecked

from communication.actuator.AsyncActuatorCommands import AsyncActuatorCommands
from .BaseStrategy import BaseStrategy
from repository.ActuatorsRepository import ActuatorsRepository


class GroupStrategy(BaseStrategy):
    @typechecked()
    def __init__(self, actuators_repo: ActuatorsRepository, job_controll: AsyncActuatorCommands):
        self.__job_controll = job_controll
        self.__actuators_repo = actuators_repo

    @typechecked()
    def supports(self, actuator_name: str) -> bool:
        return self.__actuators_repo.get_actuators()[actuator_name].strategy == 'group'

    @typechecked()
    def toggle(self, actuator_name: str, state: bool) -> bool:
        raise Exception("Not implemented")
        toggle_actuators = self.actuators_config[actuator_name]['actuators']
        future_state = self.actuators_config[actuator_name]['futureState']
        for actuator_name in toggle_actuators:
            self.__job_controll.change_actuator(actuator_name, future_state)

        return True