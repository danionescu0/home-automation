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
        command = self.__calculate_actuator_command(actuator_name, state)
        self.communicator.send(device_name, command)
        print device_name, command

    def __close_all_lights(self):
        allActuators = self.data_container.get_actuators()
        for name, propreties in allActuators.iteritems():
            if propreties['device'] == 'light':
                self.data_container.set_actuator(name, False)
                self.__do_change_actuator(name, False)
                time.sleep(3)

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