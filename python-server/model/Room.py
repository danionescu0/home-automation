from typeguard import typechecked


class Room:
    @typechecked()
    def __init__(self, id: str, name: str, sensors, actuators) -> None:
        self.id = id
        self.name = name
        self.sensors = sensors
        self.actuators = actuators

    def __repr__(self) -> str:
        return "Room: id({0}), name({1}), sensors({2}), actuators({3})," .format(self.id, self.name, self.sensors,
                                                                    self.actuators)