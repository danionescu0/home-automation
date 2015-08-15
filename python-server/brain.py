
class brain:
    def __init__(self, btComm, serial, dataContainer, emailNotificator):
        self.btComm = btComm
        self.serial = serial
        self.dataContainer = dataContainer
        self.emailNotificator = emailNotificator

    def changeActuator(self, actuator, state):
        self.dataContainer.setActuator(actuator, state)
        if actuator == 'door':
            self.serial.write("0")
        if actuator == 'livingLight':
            self.serial.write("1")
            self.__writeActuatorState(state)
        if actuator == 'bedroomLight':
            self.serial.write("2")
            self.__writeActuatorState(state)
        if actuator == 'holwayLight':
            self.serial.write("3")
            self.__writeActuatorState(state)
        if actuator == 'kitchenLight':
            self.serial.write("4")
            self.__writeActuatorState(state)
        if actuator == 'window':
            if state:
               self.btComm['bedroom'].send("1")
            else:
               self.btComm['bedroom'].send("0")

    def __writeActuatorState(self, state):
        if (state):
            self.serial.write("O")
        else:
            self.serial.write("C")
        self.serial.write("|");

    def sensorsUpdate(self, name):
        sensors = self.dataContainer.getSensors()
        actuators = self.dataContainer.getActuators()
        if name == 'rain' and sensors['rain'] > 30 and actuators['window']['state'] == False:
            self.btComm['bedroom'].send("1")
            actuators['window']['state'] = True
            self.dataContainer.setActuator('window', True)
        if actuators['homeAlarm']['state'] == True and name == 'presence' and sensors['presence'] == 1:
            self.emailNotificator.sendAlert("Cineva a intrat in casa", "Nasol naspa")
