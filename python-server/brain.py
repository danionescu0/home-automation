class brain:
    def __init__(self, btComm, serial):
        self.btComm = btComm
        self.serial = serial

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

    def sensorsUpdate(self, sensors, actuators, name):
        if name == 'rain' and sensors['rain'] > 30 and actuators['window'] == False:
            self.btComm['bedroom'].send("1")
            actuators['window'] = True
        return actuators
