import time

from BaseStrategy import BaseStrategy

class SendStrategy(BaseStrategy):
    def __init__(self, communicator_registry, actuators_config, actuators_repo):
        super(SendStrategy, self).__init__(actuators_config)
        self.__communicator_registry = communicator_registry
        self.__actuators_repo = actuators_repo

    def supports(self, actuator_name):
        return self.actuators_config[actuator_name]['strategy'] == 'send'

    def toggle(self, actuator_name, state):
        if actuator_name == 'closeAllLights':
            self.__close_all_lights()
            return
        device_name = self.actuators_config[actuator_name]['send_to_device']
        if self.__should_execute_command(actuator_name):
            command = self.__calculate_actuator_command(actuator_name, state)
            communicator_name = self.actuators_config[actuator_name]['communicator']
            self.__communicator_registry. \
                get_communicator(communicator_name). \
                send(device_name, command)


    def __close_all_lights(self):
        all_actuators = self.__actuators_repo.get_actuators()
        for actuator_name, propreties in all_actuators.iteritems():
            if propreties['device_type'] == 'light':
                self.__actuators_repo.set_actuator(actuator_name, False)
                self.change_actuator(actuator_name, False)
                time.sleep(3)

    def __should_execute_command(self, actuator_name):
        actuator_details = self.actuators_config[actuator_name]
        if actuator_details['command'] != False:
            return True

        return False

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