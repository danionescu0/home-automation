import time

class ActuatorCommands:
    def __init__(self, communicator, data_container, actuators_config):
        self.communicator = communicator
        self.data_container = data_container
        self.__actuators_config = actuators_config

    def change_actuator(self, actuator_name, state):
        self.data_container.set_actuator(actuator_name, state)
        if actuator_name == 'closeAllLights':
            self.__close_all_lights()
            return
        device_name = self.__actuators_config[actuator_name]['send_to_device']
        if self.__should_execute_command(actuator_name):
            command = self.__calculate_actuator_command(actuator_name, state)
            self.communicator.send(device_name, command)

    def __close_all_lights(self):
        all_actuators = self.data_container.get_actuators()
        for actuator_name, propreties in all_actuators.iteritems():
            if propreties['device_type'] == 'light':
                self.data_container.set_actuator(actuator_name, False)
                self.change_actuator(actuator_name, False)
                time.sleep(3)

    def __should_execute_command(self, actuator_name):
        actuator_details = self.__actuators_config[actuator_name]
        if actuator_details['command']!= False:
            return True

        return False

    def __calculate_actuator_command(self, actuator_name, state):
        actuator_details = self.__actuators_config[actuator_name]
        actuator_type = actuator_details['type']
        actuator_command = actuator_details['command']
        if actuator_type == 'bi':
            return actuator_command[state]
        elif actuator_type == 'single':
            return actuator_command[True]
        else:
            raise Exception('unimplemented actuator type %s'.format(actuator_type))