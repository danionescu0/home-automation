from enum import Enum


class Sensors(Enum):
   TEMPERATURE = 'temperature'
   HUMIDITY = 'humidity'
   PRESSURE = 'pressure'
   RAIN = 'rain'
   LIGHT = 'light'

   @staticmethod
   def list():
       return list(map(lambda c: c.value, Sensors))