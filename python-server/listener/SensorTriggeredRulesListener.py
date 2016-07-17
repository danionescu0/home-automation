from blinker import signal

class SensorTriggeredRulesListener:
    def __init__(self, data_container, emailNotificator, actuator_commands):
        self.__dataContainer = data_container
        self.__emailNotificator = emailNotificator
        self.__actuator_commands = actuator_commands
        sensor_update =  signal("sensor_update")
        sensor_update.connect(self.callback)

    def callback(self, sensor_update):
        actuators = self.__dataContainer.get_actuators()
        sensorName = sensor_update.get_name()
        sensorValue = sensor_update.get_new_value()
        if sensorName == 'rain' and sensorValue > 40 and actuators['window']['state'] == False:
            self.__actuator_commands.change_actuator('window', True)

        if actuators['homeAlarm']['state'] == True and sensorName == 'presence' and sensorValue == 1:
            self.__emailNotificator.send_alert("Cineva a intrat in casa!", "Nasol naspa")

        if sensorName == 'fingerprint' and sensorValue > -1:
            self.__actuator_commands.change_actuator('door', True)