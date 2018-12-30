import statistics
import math
import pandas
from operator import itemgetter
import numpy

from data_processing.BaseProcessor import BaseProcessor
from model.DataFeatures import DataFeatures


class HourGroupStatsProcessor(BaseProcessor):
    def __init__(self, group_by_hours: int, sensor_names: list) -> None:
        self.__group_by_hours = group_by_hours
        self.__sensor_names = sensor_names

    def process(self, dataframe):
        dataframe_dict = {}
        for index, row in dataframe.iterrows():
            hour_group = self.__get_hour_group(row['date'])
            if hour_group not in dataframe_dict:
                dataframe_dict[hour_group] = [row.to_dict()]
            else:
                dataframe_dict[hour_group].append(row.to_dict())
        final_data = []
        for key, items in dataframe_dict.items():
            final_data.append(self.__get_important_attributes(key, items, self.__sensor_names))

        return pandas.DataFrame(final_data).set_index('_id').sort_values('date')

    def __get_important_attributes(self, key: str, items: list, sensor_names: list):
        attributes = {
            'date': items[0]['date'],
            '_id' : key,
        }
        for sensor in sensor_names:
            attributes[sensor + '_' + DataFeatures.MIN.value] = min(map(itemgetter(sensor), items))
            attributes[sensor + '_' + DataFeatures.MAX.value] = max(map(itemgetter(sensor), items))
            attributes[sensor + '_' + DataFeatures.AVERAGE.value] = statistics.mean(map(itemgetter(sensor), items))
            attributes[sensor + '_' + DataFeatures.PERCENTILE70.value] = numpy.percentile(numpy.array(list(map(itemgetter(sensor), items))), 70)
            attributes[sensor + '_' + DataFeatures.PERCENTILE90.value] = numpy.percentile(numpy.array(list(map(itemgetter(sensor), items))), 90)
            # attributes[sensor + '_' + DataFeatures.PERCENTILE30.value] = numpy.percentile(numpy.array(list(map(itemgetter(sensor), items))), 30)
            # attributes[sensor + '_' + DataFeatures.PERCENTILE10.value] = numpy.percentile(numpy.array(list(map(itemgetter(sensor), items))), 10)
            rise = fall = steady = last_value = 0
            for item in items:
                if item[sensor] > last_value:
                    rise += 1
                elif item[sensor] < last_value:
                    fall += 1
                else:
                    steady += 1
                last_value = item[sensor]
                attributes[sensor + '_' + DataFeatures.RISE.value] = rise
                attributes[sensor + '_' + DataFeatures.FALL.value] = fall
                attributes[sensor + '_' + DataFeatures.STEADY.value] = steady

        return attributes

    def __get_hour_group(self, date):
        return date.strftime('%m_%d_%Y_') + str(math.floor(date.hour / self.__group_by_hours))