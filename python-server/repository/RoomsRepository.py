from typing import List

from typeguard import typechecked

from repository.SensorsRepository import SensorsRepository
from repository.ActuatorsRepository import ActuatorsRepository
from model.Room import Room


class RoomsRepository:
    @typechecked()
    def __init__(self, sensors_repository: SensorsRepository, actuators_repository: ActuatorsRepository):
        self.__sensors_repository = sensors_repository
        self.__actuators_repository = actuators_repository

    @typechecked()
    def get_rooms(self) -> List[Room]:
        rooms = []
        sensors_by_room = self.__group_sensors()
        actuators_by_room = self.__group_actuators()

        for room_name, actuators in actuators_by_room.items():
            sensors = None
            if room_name in sensors_by_room:
                sensors = sensors_by_room[room_name]
            rooms.append(Room(room_name, room_name, sensors, actuators))
        for room_name, sensors in sensors_by_room.items():
            actuators = None
            if room_name in actuators_by_room:
                actuators = actuators_by_room[room_name]
            rooms.append(Room(room_name, room_name, sensors, actuators))

        return rooms

    def __group_actuators(self):
        actuators = self.__actuators_repository.get_actuators()
        grouped_actuators = {}
        for name, actuator in actuators.items():
            if not isinstance(actuator.room, str):
                continue
            group_key = actuator.room
            if not group_key in grouped_actuators:
                grouped_actuators[group_key] = []
            actuator_data = actuators[name]
            grouped_actuators[group_key].append(actuator_data)

        return grouped_actuators

    #Todo eliminate hack: type(sensor.location) != 'str'
    def __group_sensors(self):
        sensors = self.__sensors_repository.get_sensors()
        grouped_sensors = {}
        for sensor in sensors:
            if not isinstance(sensor.location, str):
                continue
            group_key = sensor.location
            if not group_key in grouped_sensors:
                grouped_sensors[group_key] = []
            grouped_sensors[group_key].append(sensor)

        return grouped_sensors
