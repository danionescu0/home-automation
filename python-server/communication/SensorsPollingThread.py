import threading
import time
from logging import RootLogger

from typeguard import typechecked

from repository.SensorsRepository import SensorsRepository
from event.SensorUpdateEvent import SensorUpdateEvent


class SensorsPollingThread(threading.Thread):
    @typechecked()
    def __init__(self, polling_interval: int, sensors_repo: SensorsRepository,
                 sensor_update_event: SensorUpdateEvent, logger: RootLogger):
        threading.Thread.__init__(self)
        self.__polling_interval = polling_interval
        self.__sensors_repo = sensors_repo
        self.__sensor_update_event = sensor_update_event
        self.__logger = logger
        self.shutdown = False

    @typechecked()
    def run(self) -> None:
        while not self.shutdown:
            sensors = self.__sensors_repo.get_sensors()
            time.sleep(self.__polling_interval)
