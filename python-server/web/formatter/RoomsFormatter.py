from typing import List

from repository.RoomsRepository import RoomsRepository
from model.Sensor import Sensor
from model.SensorProperties import SensorProperties
from model.Actuator import Actuator
from model.Room import Room
from model.ActuatorProperties import ActuatorProperties


class RoomsFormatter:
    def __init__(self, rooms_repository: RoomsRepository) -> None:
        self.__rooms_repository = rooms_repository

    def get_rooms(self) -> list:
        raw_data = self.__rooms_repository.get_rooms()
        formatted = []
        for room in raw_data:
            if room.sensors is None:
                sensors = []
            else:
                sensors = self.__get_formatted_sensors(room.sensors)
            if room.actuators is None:
                actuators = []
            else:
                actuators = self.__get_formatted_actuators(room, room.actuators)
            formatted.append({
                'id' : room.id,
                'name' : self.__get_room_name(room.name),
                'actuators' : actuators,
                'sensors' : sensors
            })

        return formatted

    def __get_room_name(self, unformatted_name):
        return unformatted_name[0].upper() + unformatted_name[1:]

    def __get_formatted_actuators(self, room: Room, actuators: List[Actuator]) -> list :
        formatted = []
        for actuator in actuators:
            formatted.append({
                'type' : actuator.type,
                'id' : actuator.id,
                'name' : self.__get_actuator_name(room, actuator),
                'value' : actuator.value
            })

        return formatted

    def __get_actuator_name(self, room: Room, actuator: Actuator):
        if None is not actuator.properties.get(ActuatorProperties.SHORTCUT):
            return '[{0}] {1}'.format(self.__get_room_name(actuator.room), actuator.name)

        return actuator.name

    def __get_formatted_sensors(self, sensors: List[Sensor]) -> list:
        formatted = []
        for sensor in sensors:
            formatted.append({
                'type' : sensor.type,
                'id' : sensor.id,
                'name' : self.__get_formatted_sensor_name(sensor),
                'value' : sensor.value
            })

        return formatted

    def __get_formatted_sensor_name(self, sensor: Sensor) -> str:
        sensor_name = sensor.properties.get(SensorProperties.NAME)
        if None is not sensor_name:
            return sensor_name

        return '{0} {1}'.format(sensor.type, sensor.location)