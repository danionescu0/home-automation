import collections
from typing import List

from typeguard import typechecked

from repository.SensorsRepository import SensorsRepository
from repository.ActuatorsRepository import ActuatorsRepository
from model.Room import Room
from model.ActuatorProperties import ActuatorProperties
from model.SensorProperties import SensorProperties


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
        room_names = self.__get_room_names(sensors_by_room, actuators_by_room)

        for room_name in room_names:
            sensors = sensors_by_room[room_name] if room_name in sensors_by_room else []
            actuators = actuators_by_room[room_name] if room_name in actuators_by_room else []
            rooms.append(Room(room_name, room_name, sensors, actuators))

        return rooms

    def __get_room_names(self, sensors_by_room, actuators_by_room):
        room_names = collections.OrderedDict.fromkeys(
            [Room.MOST_FREQUENTLY_USED_ROOM] + list(sensors_by_room.keys()) + list(actuators_by_room.keys())
        )

        return [key for key, value in room_names.items()]

    def __group_actuators(self):
        actuators = self.__actuators_repository.get_actuators()
        grouped_actuators = {}
        for name, actuator in actuators.items():
            group_key = actuator.room
            if not group_key in grouped_actuators:
                grouped_actuators[group_key] = []
            if not Room.MOST_FREQUENTLY_USED_ROOM in grouped_actuators:
                grouped_actuators[Room.MOST_FREQUENTLY_USED_ROOM] = []
            actuator_data = actuators[name]
            grouped_actuators[group_key].append(actuator_data)
            if None is not actuator.properties.get(ActuatorProperties.SHORTCUT):
                grouped_actuators[Room.MOST_FREQUENTLY_USED_ROOM].append(actuator_data)

        return grouped_actuators

    def __group_sensors(self):
        sensors = self.__sensors_repository.get_sensors()

        grouped_sensors = {}
        for sensor in sensors:
            group_key = sensor.location
            if not group_key in grouped_sensors:
                grouped_sensors[group_key] = []
            if not Room.MOST_FREQUENTLY_USED_ROOM in grouped_sensors:
                grouped_sensors[Room.MOST_FREQUENTLY_USED_ROOM] = []
            grouped_sensors[group_key].append(sensor)
            if None is not sensor.properties.get(SensorProperties.SHORTCUT):
                grouped_sensors[Room.MOST_FREQUENTLY_USED_ROOM].append(sensor)

        return grouped_sensors