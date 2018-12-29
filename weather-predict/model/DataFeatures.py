from enum import Enum


class DataFeatures(Enum):
   AVERAGE = 'avg'
   RISE = 'rise'
   FALL = 'fall'
   STEADY = 'steady'
   MIN = 'min'
   MAX = 'max'
   # STDEV = 'stdev'

   @staticmethod
   def list():
       return list(map(lambda c: c.value, DataFeatures))