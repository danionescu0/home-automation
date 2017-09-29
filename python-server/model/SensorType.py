from enum import Enum


class SensorType(Enum):
    HUMIDITY = 'humidity'
    TEMPERATURE = 'temperature'
    AIR_PRESSURE = 'airPressure'
    LIGHT = 'light'
    VOLTAGE = 'voltage'
    RAIN = 'rain'
    PRESENCE = 'presence'
    AIR_POLLUTION = 'airPollution'
    FINGERPRINT = 'fingerprint'
    PHONE_IS_HOME = 'phoneIsHome'
    POWER = 'power'