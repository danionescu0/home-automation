import threading

class IncommingCommunicationThread(threading.Thread):
    def __init__(self, text_sensor_data_parser, sensors_repo, sensor_update_event, communicator):
        threading.Thread.__init__(self)
        self.__text_sensor_data_parser = text_sensor_data_parser
        self.__sensors_repo = sensors_repo
        self.__sensor_update_event = sensor_update_event
        self.__communicator = communicator
        self.shutdown = False

    def run(self):
        while not self.shutdown:
            self.__communicator.listen(self.__text_sensor_data_parser.is_buffer_parsable,
                                       self.__sensor_callback)
        self.__communicator.disconnect()

    def __sensor_callback(self, message):
        sensors = self.__text_sensor_data_parser.parse(message)
        for sensor in sensors:
            self.__sensors_repo.set_sensor(sensor['type'], sensor['location'], sensor['value'])
            self.__sensor_update_event.send(sensor['type'], sensor['location'], sensor['value'])
