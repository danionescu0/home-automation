import threading
import time
from typeguard import typechecked

from communication.TextSensorDataParser import TextSensorDataParser
from repository.Sensors import Sensors
from event.SensorUpdateEvent import SensorUpdateEvent
from communication.Base import Base

class IncommingCommunicationThread(threading.Thread):
    LISTEN_DELAY = 0.01

    @typechecked()
    def __init__(self, text_sensor_data_parser: TextSensorDataParser, sensors_repo: Sensors,
                 sensor_update_event: SensorUpdateEvent,communicator: Base):
        threading.Thread.__init__(self)
        self.__text_sensor_data_parser = text_sensor_data_parser
        self.__sensors_repo = sensors_repo
        self.__sensor_update_event = sensor_update_event
        self.__communicator = communicator
        self.shutdown = False

    @typechecked()
    def run(self) -> None:
        while not self.shutdown:
            self.__communicator.listen(self.__text_sensor_data_parser.is_buffer_parsable,
                                       self.__sensor_callback)
            time.sleep(self.LISTEN_DELAY)
        self.__communicator.disconnect()

    def __sensor_callback(self, message):
        sensors = self.__text_sensor_data_parser.parse(message)
        for sensor in sensors:
            self.__sensors_repo.set_sensor(sensor['type'], sensor['location'], sensor['value'])
            self.__sensor_update_event.send(sensor['type'], sensor['location'], sensor['value'])
