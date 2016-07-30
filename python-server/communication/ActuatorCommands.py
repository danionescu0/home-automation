import time

class ActuatorCommands:
    def __init__(self, communicator, data_container):
        self.communicator = communicator
        self.data_container = data_container

    def change_actuator(self, actuator, state):
        self.data_container.set_actuator(actuator, state)
        if actuator != 'closeAllLights':
            self.__do_change_actuator(actuator, state)
            return

        allActuators = self.data_container.get_actuators()
        for name, propreties in allActuators.iteritems():
            if propreties['device'] == 'light':
                self.data_container.set_actuator(name, False)
                self.__do_change_actuator(name, False)
                time.sleep(3)

    def __do_change_actuator(self, actuator, state):
        lights = {
            'livingLight' : '1', 'bedroomLight' : '2',
            'holwayLight' : '3', 'kitchenLight' : '4',
            'closetLight' : '5', 'balconyLight' : '6'
        }
        if actuator == 'door':
            self.communicator.send('holway', 'O')
        if actuator in lights:
            self.communicator.send('living', lights[actuator])
            self.__write_actuator_state(state)
        if actuator == 'powerSocket1':
            self.communicator.send('living', '8')
            self.__write_actuator_state(state)
        if actuator == 'livingCourtains':
            if state:
                self.communicator.send('balcony', '1')
            else:
                self.communicator.send('balcony', '0')
        if actuator == 'windowNodgeDown':
            self.communicator.send('bedroom', '2')
        if actuator == 'window':
            if state:
                self.communicator.send('bedroom', '1')
            else:
                self.communicator.send('bedroom', '0')

    def __write_actuator_state(self, state):
        if (state):
            self.communicator.send('living', 'O')
        else:
            self.communicator.send('living', 'C')
        self.communicator.send('living', '|')