import time

class ActuatorCommands:
    def __init__(self, btComm, dataContainer):
        self.btComm = btComm
        self.dataContainer = dataContainer
        self.lastBurglerLight = None
        self.burglerLights = ['livingLight', 'kitchenLight', 'bedroomLight']
        self.burglerMaxWaitBetweenActions = 3
        self.burglerSounds = 2

    def changeActuator(self, actuator, state):
        self.dataContainer.setActuator(actuator, state)
        if actuator != 'closeAllLights':
            self.__doChangeActuator(actuator, state)
            return

        allActuators = self.dataContainer.getActuators()
        for name, propreties in allActuators.iteritems():
            if propreties['device'] == 'light':
                self.dataContainer.setActuator(name, False)
                self.__doChangeActuator(name, False)
                time.sleep(3)

    def __doChangeActuator(self, actuator, state):
        lights = {
            'livingLight' : '1', 'bedroomLight' : '2',
            'holwayLight' : '3', 'kitchenLight' : '4',
            'closetLight' : '5', 'balconyLight' : '6'
        }
        if actuator == 'door':
            self.btComm.send('holway', 'O')
        if actuator in lights:
            self.btComm.send('living', lights[actuator])
            self.__writeActuatorState(state)
        if actuator == 'powerSocket1':
            self.btComm.send('living', '8')
            self.__writeActuatorState(state)
        if actuator == 'livingCourtains':
            if state:
                self.btComm.send('balcony', '1')
            else:
                self.btComm.send('balcony', '0')
        if actuator == 'windowNodgeDown':
            self.btComm.send('bedroom', '2')
        if actuator == 'window':
            if state:
                self.btComm.send('bedroom', '1')
            else:
                self.btComm.send('bedroom', '0')

    def __writeActuatorState(self, state):
        if (state):
            self.btComm.send('living', 'O')
        else:
            self.btComm.send('living', 'C')
        self.btComm.send('living', '|')