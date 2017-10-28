import time

from typeguard import typechecked

from .BaseStrategy import BaseStrategy
from communication.SerialCommunicatorRegistry import SerialCommunicatorRegistry
from repository.ActuatorsRepository import ActuatorsRepository
from model.Actuator import Actuator


class SerialSendStrategy(BaseStrategy):
    @typechecked()
    def __init__(self, communicator_registry: SerialCommunicatorRegistry, actuators_repo: ActuatorsRepository):
        self.__communicator_registry = communicator_registry
        self.__actuators_repo = actuators_repo

    @typechecked()
    def supports(self, actuator_name: str) -> bool:
        return self.__actuators_repo.get_actuators()[actuator_name].strategy == 'send'

    @typechecked()
    def toggle(self, actuator_name:str , state: bool):
        actuator = self.__actuators_repo.get_actuators()[actuator_name]
        command = self.get_encriptor().encrypt(self.__calculate_actuator_command(actuator, state))
        self.__communicator_registry. \
            get_communicator(actuator.communicator). \
            send(actuator.send_to_device, command)
        time.sleep(0.5)

        return True

    # todo remove this hack: actuator_command[{True: 'true', False: 'false'}[state]]
    def __calculate_actuator_command(self, actuator: Actuator, state: bool):
        actuator_type = actuator.type
        actuator_command = actuator.command
        print(actuator_command)
        if actuator_type == 'bi':
            return actuator_command[{True: 'true', False: 'false'}[state]]
        elif actuator_type == 'single':
            return actuator_command['true']
        else:
            raise Exception('Unimplemented actuator type: %s'.format(actuator_type))