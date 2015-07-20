
class brain:
    def __init__(self, btComm, serial, dataContainer):
        self.btComm = btComm
        self.serial = serial
        self.dataContainer = dataContainer

    def changeActuator(self, actuator, state):
        if actuator == 'door':
            self.serial.write("3")
        if actuator == 'livingLight':
            self.serial.write("1")
        if actuator == 'bedroomLight':
            self.serial.write("2")
        if actuator == 'window':
            if state == 'on':
               self.btComm['bedroom'].send("1")
            else:
               self.btComm['bedroom'].send("0")

    def sensorsUpdate(self, name):
        sensors = self.dataContainer.getSensors()
        actuators = self.dataContainer.getActuators()
        if name == 'rain' and sensors['rain'] > 30 and actuators['window'] == False:
            self.btComm['bedroom'].send("1")
            actuators['window'] = True
            self.dataContainer.setActuator('window', True)
