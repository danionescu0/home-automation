from blinker import signal

class sensorTriggeredRulesListener:
    def __init__(self, dataContainer, emailNotificator, brain):
        self.__dataContainer = dataContainer
        self.__emailNotificator = emailNotificator
        self.__brain = brain
        sensorUpdate =  signal("sensor_update")
        sensorUpdate.connect(self.callback)

    def callback(self, sensorUpdate):
        actuators = self.__dataContainer.getActuators()
        sensorName = sensorUpdate.getName()
        sensorValue = sensorUpdate.getNewValue()
        if sensorName == 'rain' and sensorValue > 40 and actuators['window']['state'] == False:
            self.__brain.changeActuator('window', True)

        if actuators['homeAlarm']['state'] == True and sensorName == 'presence' and sensorValue == 1:
            self.__emailNotificator.sendAlert("Cineva a intrat in casa!", "Nasol naspa")

        if sensorName == 'fingerprint' and sensorValue > -1:
            self.__brain.changeActuator('door', True)