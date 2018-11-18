import time

from typeguard import typechecked

from communication.AesEncriptor import AesEncriptor
from communication.DeviceLifetimeManager import DeviceLifetimeManager
from communication.actuator.strategies.BaseStrategy import BaseStrategy
from model.Actuator import Actuator
from model.ActuatorProperties import ActuatorProperties


class SerialSendStrategy(BaseStrategy):
    @typechecked()
    def __init__(self, device_lifetime_manager: DeviceLifetimeManager, encriptor: AesEncriptor, logger):
        self.__device_lifetime_manager = device_lifetime_manager
        self.__encriptor = encriptor
        self.__logger = logger

    @typechecked()
    def supports(self, actuator: Actuator) -> bool:
        return actuator.device_type == Actuator.DeviceType.SERIAL.value \
               and actuator.type in [Actuator.ActuatorType.SWITCH.value, Actuator.ActuatorType.PUSHBUTTON.value]

    @typechecked()
    def set_state(self, actuator: Actuator, state):
        command = self.__encrypt(self.__calculate_actuator_command(actuator, state), actuator)
        if command is False:
            return False
        send_to_device = actuator.properties.get(ActuatorProperties.SEND_TO_DEVICE)
        communicator = actuator.properties.get(ActuatorProperties.COMMUNICATOR)
        self.__device_lifetime_manager. \
            get_device(communicator). \
            send(send_to_device, command)
        time.sleep(0.5)

        return True

    def __calculate_actuator_command(self, actuator: Actuator, state: bool):
        actuator_type = actuator.type
        actuator_command = actuator.properties.get(ActuatorProperties.COMMAND)
        if actuator_type == Actuator.ActuatorType.SWITCH.value:
            return actuator_command[{True: 'true', False: 'false'}[state]]
        elif actuator_type == Actuator.ActuatorType.PUSHBUTTON.value:
            return actuator_command['true']
        else:
            return False

    def __encrypt(self, text: str, actuator: Actuator):
        encription = actuator.properties.get(ActuatorProperties.ENCRIPTION)
        if None is encription:
            return str.encode(text)

        return self.__encriptor.encrypt(text)


