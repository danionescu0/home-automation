import threading
import time
from logging import RootLogger

from typeguard import typechecked

from repository.SensorsRepository import SensorsRepository
from model.Sensor import Sensor
from model.SensorProperties import SensorProperties
from event.SensorUpdateEvent import SensorUpdateEvent
from communication.ZWaveDevice import ZWaveDevice


class SensorsPollingThread(threading.Thread):
    @typechecked()
    def __init__(self, polling_interval: int, sensors_repo: SensorsRepository, zwave_device: ZWaveDevice,
                 sensor_update_event: SensorUpdateEvent, logger: RootLogger):
        threading.Thread.__init__(self)
        self.__polling_interval = polling_interval
        self.__sensors_repo = sensors_repo
        self.__zwave_device = zwave_device
        self.__sensor_update_event = sensor_update_event
        self.__logger = logger
        self.shutdown = False

    @typechecked()
    def run(self) -> None:
        while not self.shutdown:
            self.__update_sensors()
            time.sleep(self.__polling_interval)

    def __update_sensors(self):
        sensors = self.__sensors_repo.get_sensors()
        for sensor in sensors:
            if None is sensor.properties.get(SensorProperties.POLLING):
                continue
            if sensor.device_type == Sensor.DeviceType.ZWAVE.value:
                self.__update_zwave_sensor(sensor)

    def __update_zwave_sensor(self, sensor: Sensor):
        new_value = self.__zwave_device.get_sensor_value(sensor.id)
        self.__logger.info("New value for sensor with id {0} is {1}: ".format(sensor.id, new_value))
        if None is not new_value:
            sensor.value = round(new_value, 1)
            self.__sensors_repo.set_sensor(sensor)
            self.__sensor_update_event.send(sensor)
