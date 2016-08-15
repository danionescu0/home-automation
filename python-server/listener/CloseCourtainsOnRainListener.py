from blinker import signal

class CloseCourtainsOnRainListener:
    __RAIN_SENSOR_THRESHOLD = 40

    def __init__(self, actuators_repo, actuator_commands):
        self.__actuators_repo = actuators_repo
        self.__actuator_commands = actuator_commands
        sensor_update =  signal("sensor_update")
        sensor_update.connect(self.callback)

    def callback(self, sensor_update):
        if self.__should_close_courtains(sensor_update):
            self.__actuator_commands.change_actuator('bedroomCourtains', True)

    def __should_close_courtains(self, sensor_update):
        sensor_name = sensor_update.get_name()
        sensor_value = sensor_update.get_new_value()

        return  sensor_name == 'rain' and sensor_value > self.__RAIN_SENSOR_THRESHOLD and self.__is_window_actuator_open()

    def __is_window_actuator_open(self):
        actuators = self.__actuators_repo.get_actuators()

        return actuators['bedroomCourtains']['state'] == False