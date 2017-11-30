from typeguard import typechecked

from repository.ActuatorsRepository import ActuatorsRepository


class ActuatorsFormatter:
    @typechecked()
    def __init__(self, actuators_repository: ActuatorsRepository) -> None:
        self.__actuators_repository = actuators_repository

    @typechecked()
    def get_all(self) -> list:
        actuators = self.__actuators_repository.get_actuators()

        return [{
            'id': id,
            'name' : actuator.name,
            'value' : actuator.value,
            'type' : actuator.type,
            'room' : actuator.room,
            'device_type' : actuator.device_type,
        } for id, actuator in actuators.items()]