from BaseStrategy import BaseStrategy
import time

class SerialSendStrategy(BaseStrategy):
    def __init__(self, communicator_registry, actuators_config, actuators_repo):
        super(SerialSendStrategy, self).__init__(actuators_config)
        self.__communicator_registry = communicator_registry
        self.__actuators_repo = actuators_repo

    def supports(self, actuator_name):
        return self.actuators_config[actuator_name]['strategy'] == 'send'

    def toggle(self, actuator_name, state):
        device_name = self.actuators_config[actuator_name]['send_to_device']
        command = self.get_encriptor().encrypt(self.__calculate_actuator_command(actuator_name, state))
        communicator_name = self.actuators_config[actuator_name]['communicator']
        self.__communicator_registry. \
            get_communicator(communicator_name). \
            send(device_name, command)
        time.sleep(0.5)

        return True

    def __calculate_actuator_command(self, actuator_name, state):
        actuator_details = self.actuators_config[actuator_name]
        actuator_type = actuator_details['type']
        actuator_command = actuator_details['command']
        if actuator_type == 'bi':
            return actuator_command[state]
        elif actuator_type == 'single':
            return actuator_command[True]
        else:
            raise Exception('unimplemented actuator type %s'.format(actuator_type))