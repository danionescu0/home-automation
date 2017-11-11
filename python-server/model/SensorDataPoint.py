class SensorDataPoint:
    def __init__(self, value, timestamp: int) -> None:
        self.value = value
        self.timestamp = timestamp

    def __repr__(self) -> str:
        return "Sensor datapoint: value({0}), timestamp({1})" . format(self.value, self.timestamp)