class Sensor:
    def __init__(self, type: str, value: float) -> None:
        self.type = type
        self.value = value

    def __repr__(self) -> str:
        return 'Sensor: type({0}), value({1})'.format(self.type, str(self.value))