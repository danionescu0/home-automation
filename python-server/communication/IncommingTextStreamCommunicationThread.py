import threading
import time
from logging import RootLogger

from typeguard import typechecked

from communication.TextSensorDataParser import TextSensorDataParser
from communication.BaseSerial import BaseSerial
from repository.SensorsRepository import SensorsRepository
from event.SensorUpdateEvent import SensorUpdateEvent
from communication.SensorsParseException import SensorsParseException


class IncommingTextStreamCommunicationThread(threading.Thread):
    LISTEN_DELAY = 0.01

    @typechecked()
    def __init__(self, text_sensor_data_parser: TextSensorDataParser, sensors_repo: SensorsRepository,
                 sensor_update_event: SensorUpdateEvent, communicator: BaseSerial, logger: RootLogger):
        threading.Thread.__init__(self)
        self.__text_sensor_data_parser = text_sensor_data_parser
        self.__sensors_repo = sensors_repo
        self.__sensor_update_event = sensor_update_event
        self.__communicator = communicator
        self.__logger = logger
        self.shutdown = False

    @typechecked()
    def run(self) -> None:
        while not self.shutdown:
            self.__communicator.listen(self.__text_sensor_data_parser.is_buffer_parsable,
                                       self.__sensor_callback)
            time.sleep(self.LISTEN_DELAY)
        self.__communicator.disconnect()

    def __sensor_callback(self, message):
        try:
            sensors = self.__text_sensor_data_parser.parse(message)
        except SensorsParseException as e:
            self.__logger.error(str(e))
            return

        for sensor in sensors:
            self.__sensors_repo.set_sensor(sensor)
            self.__sensor_update_event.send(sensor)