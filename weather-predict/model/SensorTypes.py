from enum import Enum


class SensorTypes(Enum):
   TEMPERATURE = 'temperature'
   HUMIDITY = 'humidity'
   PRESSURE = 'pressure'
   RAIN = 'rain'
   LIGHT = 'light'

   @staticmethod
   def list():
       return list(map(lambda c: c.value, SensorTypes))