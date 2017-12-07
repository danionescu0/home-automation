import threading
from logging import RootLogger

from typeguard import typechecked

from repository.SensorsRepository import SensorsRepository
from event.SensorUpdateEvent import SensorUpdateEvent
from communication.ZWaveDevice import ZWaveDevice


class IncommingZwaveCommunicationThread(threading.Thread):
    @typechecked()
    def __init__(self, sensor_update_event: SensorUpdateEvent, sensors_repository: SensorsRepository,
                 zwave_device: ZWaveDevice, logger: RootLogger):
        threading.Thread.__init__(self)
        self.__sensor_update_event = sensor_update_event
        self.__sensors_repository = sensors_repository
        self.__zwave_device = zwave_device
        self.__logger = logger
        self.shutdown = False

    def run(self) -> None:
        self.__zwave_device.attach_state_change_callback(self.__receive_zwave_device_update)

    def __receive_zwave_device_update(self, id: str, value: float):
        sensors = self.__sensors_repository.get_sensors()
        filtered = [sensor for sensor in sensors if sensor.id == id]
        if 0 == len(filtered):
            self.__logger.debug('device with id {0} not found'.format(id))
            return
        sensor = filtered[0]
        self.__logger.debug(sensor)
        sensor.value = round(value, 3)
        self.__sensors_repository.set_sensor(sensor)
        self.__sensor_update_event.send(sensor)