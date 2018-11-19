import threading
import time
from logging import RootLogger

from typeguard import typechecked
from pydispatch import dispatcher

from communication.BaseSerial import BaseSerial
from communication.SensorFromTextFactory import SensorFromTextFactory
from communication.exception.SensorsParseException import SensorsParseException
from communication.exception.SerialDecodeException import SerialDecodeException
from event.SensorUpdateEvent import SensorUpdateEvent
from repository.SensorsRepository import SensorsRepository


class IncommingTextStreamCommunicationThread(threading.Thread):
    LISTEN_DELAY = 0.01

    @typechecked()
    def __init__(self, sensor_from_text_factory: SensorFromTextFactory, sensors_repo: SensorsRepository,
                 communicator: BaseSerial, logger: RootLogger):
        threading.Thread.__init__(self)
        self.__sensor_from_text_factory = sensor_from_text_factory
        self.__sensors_repo = sensors_repo
        self.__communicator = communicator
        self.__logger = logger
        self.shutdown = False

    @typechecked()
    def run(self) -> None:
        while not self.shutdown:
            try:
                self.__communicator.listen(self.__sensor_from_text_factory.can_create, self.__sensor_callback)
            except SerialDecodeException as e:
                self.__logger.error("Could not parse incomming serial buffer: " + str(e))
            time.sleep(self.LISTEN_DELAY)

    def __sensor_callback(self, message):
        try:
            sensors = self.__sensor_from_text_factory.create(message)
        except SensorsParseException as e:
            self.__logger.error(str(e))
            return
        for sensor in sensors:
            self.__sensors_repo.set_sensor(sensor)
            dispatcher.send(SensorUpdateEvent.NAME, event=SensorUpdateEvent(sensor))