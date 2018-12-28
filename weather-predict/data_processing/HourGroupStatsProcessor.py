import statistics
import math
import pandas
from operator import itemgetter

from data_processing.BaseProcessor import BaseProcessor


class HourGroupStatsProcessor(BaseProcessor):
    def __init__(self, group_by_hours: int) -> None:
        self.__group_by_hours = group_by_hours

    def process(self, dataframe):
        dataframe_dict = {}
        for index, row in dataframe.iterrows():
            hour_group = self.__get_hour_group(row['date'])
            if hour_group not in dataframe_dict:
                dataframe_dict[hour_group] = [row.to_dict()]
            else:
                dataframe_dict[hour_group].append(row.to_dict())
        final_data = []
        sensor_names = ['light', 'rain', 'temperature', 'pressure', 'humidity']
        for key, items in dataframe_dict.items():
            final_data.append(self.__get_important_attributes(key, items, sensor_names))

        return pandas.DataFrame(final_data).set_index('_id').sort_values('date')

    def __get_important_attributes(self, key: str, items: list, sensor_names: list):
        attributes = {
            'date': items[0]['date'],
            '_id' : key,
        }
        for sensor in sensor_names:
            attributes[sensor + '_min'] = min(map(itemgetter(sensor), items))
            attributes[sensor + '_max'] = max(map(itemgetter(sensor), items))
            mean = statistics.mean(map(itemgetter(sensor), items))
            #try a fix for this
            attributes[sensor + '_avg'] = mean if not math.isnan(mean) else 0
            rise = fall = last_value = 0
            for item in items:
                if item[sensor] > last_value:
                    rise += 1
                elif item[sensor] < last_value:
                    fall += 1
                last_value = item[sensor]
                attributes[sensor + '_rise'] = rise
                attributes[sensor + '_fall'] = fall

        return attributes

    def __get_hour_group(self, date):
        return date.strftime('%m_%d_%Y_') + str(math.floor(date.hour / self.__group_by_hours))