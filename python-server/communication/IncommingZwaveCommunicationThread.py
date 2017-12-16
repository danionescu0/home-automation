import threading
from logging import RootLogger

from typeguard import typechecked

from repository.SensorsRepository import SensorsRepository
from repository.ActuatorsRepository import ActuatorsRepository
from event.SensorUpdateEvent import SensorUpdateEvent
from communication.ZWaveDevice import ZWaveDevice
from model.Sensor import Sensor
from model.Actuator import Actuator


class IncommingZwaveCommunicationThread(threading.Thread):
    @typechecked()
    def __init__(self, sensor_update_event: SensorUpdateEvent, sensors_repository: SensorsRepository,
                 actuators_repository: ActuatorsRepository, zwave_device: ZWaveDevice, logger: RootLogger):
        threading.Thread.__init__(self)
        self.__sensor_update_event = sensor_update_event
        self.__sensors_repository = sensors_repository
        self.__actuators_repository = actuators_repository
        self.__zwave_device = zwave_device
        self.__logger = logger
        self.shutdown = False

    def run(self) -> None:
        self.__zwave_device.attach_state_change_callback(self.__receive_zwave_device_update)

    @typechecked()
    def __receive_zwave_device_update(self, id: str, value):
        self.__logger.info('Checking device with id {0} and value : {1}'.format(id, value))
        sensor = self.__sensors_repository.get_sensor(id)
        if None is not sensor:
            self.__logger.debug('Sensor is {0}'.format(sensor))
            self.__process_sensor(sensor, value)
        actuator = self.__actuators_repository.get_actuator(id)
        if None is not actuator:
            self.__logger.info('Actuator is {0}'.format(actuator))
            self.__process_actuator(actuator, value)

    def __process_sensor(self, sensor: Sensor, value):
        sensor.value = round(value, 3)
        self.__sensors_repository.set_sensor(sensor)
        self.__sensor_update_event.send(sensor)

    def __process_actuator(self, actuator: Actuator, value):
        self.__actuators_repository.set_actuator_state(actuator.id, value)