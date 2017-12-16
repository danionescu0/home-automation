from typing import List

from repository.RoomsRepository import RoomsRepository
from model.Sensor import Sensor
from model.Actuator import Actuator


class RoomsFormatter:
    def __init__(self, rooms_repository: RoomsRepository) -> None:
        self.__rooms_repository = rooms_repository

    def get_rooms(self) -> list:
        raw_data = self.__rooms_repository.get_rooms()
        formatted = []
        for room in raw_data:
            if room.sensors == None:
                sensors = []
            else:
                sensors = self.__get_formatted_sensors(room.sensors)
            if room.actuators == None:
                actuators = []
            else:
                actuators = self.__get_formatted_actuators(room.actuators)
            formatted.append({
                'id' : room.id,
                'name' : room.name[0].upper() + room.name[1:],
                'actuators' : actuators,
                'sensors' : sensors
            })

        return formatted

    def __get_formatted_actuators(self, actuators: List[Actuator]) -> list :
        formatted = []
        for actuator in actuators:
            formatted.append({
                'type' : actuator.type,
                'id' : actuator.id,
                'name' : actuator.name,
                'value' : actuator.value
            })

        return formatted

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
        return sensor.name if not None == Sensor.name else '{0} {1}'.format(sensor.type, sensor.location)