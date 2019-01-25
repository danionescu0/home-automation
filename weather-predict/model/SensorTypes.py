from enum import Enum


class SensorTypes(Enum):
   TEMPERATURE = 'temperature'
   HUMIDITY = 'humidity'
   PRESSURE = 'pressure'
   RAIN = 'rain'
   LIGHT = 'light'
   WIND_SPEED = 'wind_speed'
   WIND_GUST = 'wind_gust'
   UV_INDEX = 'uv_index'
   VISIBILITY = 'visibility'


   @staticmethod
   def list():
       return list(map(lambda c: c.value, SensorTypes))