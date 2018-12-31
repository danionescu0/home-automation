from enum import Enum


class DataFeatures(Enum):
   AVERAGE = 'avg'
   RISE = 'rise'
   FALL = 'fall'
   STEADY = 'steady'
   MIN = 'min'
   MAX = 'max'
   PERCENTILE70 = '70percentile'
   PERCENTILE90 = '90percentile'
   PERCENTILE10 = '10percentile'
   PERCENTILE30 = '30percentile'

   @staticmethod
   def list():
       return list(map(lambda c: c.value, DataFeatures))