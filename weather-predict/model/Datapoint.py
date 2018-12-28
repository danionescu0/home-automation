from datetime import datetime


class Datapoint:
    def __init__(self, date: datetime, rain: float, humidity: float,
                 temperature: float, pressure: float, light: float) -> None:
        self.date = date
        self.rain = rain
        self.humidity = humidity
        self.temperature = temperature
        self.pressure = pressure
        self.light = light