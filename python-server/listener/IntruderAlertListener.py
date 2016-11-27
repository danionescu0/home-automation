from blinker import signal

class IntruderAlertListener:
    def __init__(self, actuators_repo, email_notificator):
        self.__actuators_repo = actuators_repo
        self.__email_notificator = email_notificator
        signal("sensor_update").connect(self.callback)

    def callback(self, sensor_update):
        if self.__should_send_alert(sensor_update):
            self.__email_notificator.send_alert("Alert", "Somebody entered the house")

    def __should_send_alert(self, sensor_update):
        actuators = self.__actuators_repo.get_actuators()
        sensor_type = sensor_update.get_type()
        sensor_value = sensor_update.get_new_value()

        return actuators['homeAlarm']['state'] == True and sensor_type == 'presence' and sensor_value == 1