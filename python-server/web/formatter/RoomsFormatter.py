from repository.RoomsRepository import RoomsRepository


class RoomsFormatter:
    def __init__(self, rooms_repository: RoomsRepository) -> None:
        self.__rooms_repository = rooms_repository

    def get_rooms(self):
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

    def __get_formatted_actuators(self, actuators):
        formatted = []
        for actuator in actuators:
            formatted.append({
                'type' : actuator.type,
                'id' : actuator.id,
                'name' : actuator.name,
                'value' : actuator.value
            })

        return formatted

    def __get_formatted_sensors(self, sensors):
        formatted = []
        for sensor in sensors:
            formatted.append({
                'type' : sensor.type,
                'id' : sensor.id,
                'name' : sensor.type + ' ' + sensor.location,
                'value' : sensor.value
            })

        return formatted