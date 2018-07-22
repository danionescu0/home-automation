import requests
import statistics
import itertools
import math
from datetime import datetime


class DataExtractor():
    def __init__(self, url: str, sensors: list, add_rise_fall_data_to_sensors: list = None) -> None:
        self.__url = url
        self.__sensors = sensors
        self.__add_rise_fall_data_to_sensors = add_rise_fall_data_to_sensors or []

    def get_for(self, date: datetime, grouped_by_hours: int):
        useful_data = []
        for sensor in self.__sensors:
            literal_date = date.strftime('%m-%d-%Y')
            data = self.get_sensor_data(literal_date, sensor)
            if not len(data) or len(data) < 130:
                continue
            grouped_by_hour = self.__grouped_by_hours_interval(data, grouped_by_hours)
            for hour_data in grouped_by_hour:
                last_group = dict()
                last_group['date'] = literal_date + ' ' + str(hour_data[0]['hour_group'])
                last_group['hour_group'] = hour_data[0]['hour_group']
                last_group[sensor + '_min'], last_group[sensor + '_max'], last_group[sensor + '_mean'] = \
                    self.__get_keypoints(hour_data)
                last_group[sensor + '_stdev'] = statistics.stdev(datapoint['value'] for datapoint in hour_data)
                # if sensor in self.__add_rise_fall_data_to_sensors:
                #     last_group[sensor + '_rise'], last_group[sensor + '_fall'] = self.__get_rise_fall(hour_data)
                useful_data.append(last_group)

        last_process = {}
        for datapoint in useful_data:
            if not datapoint['date'] in last_process:
                last_process[datapoint['date']] = datapoint
            last_process[datapoint['date']].update(datapoint)
        as_list = [value for key, value in last_process.items()]

        return sorted(as_list, key=lambda datapoint: datapoint['hour_group'])

    def get_sensor_data(self, literal_date, sensor) -> list:
        request = self.__url.format(sensor, literal_date, literal_date)
        response = requests.get(request)

        return response.json()['data']

    def __get_keypoints(self, hour_data: list) -> tuple:
        return min(datapoint['value'] for datapoint in hour_data)\
            , max(datapoint['value'] for datapoint in hour_data)\
            , statistics.mean(datapoint['value'] for datapoint in hour_data)

    def __get_rise_fall(self, hour_group: list) -> tuple:
        rise = int(len([i for i in range(1, len(hour_group)) if hour_group[i - 1]['value'] > hour_group[i]['value']])
                   / len(hour_group) * 100)
        fall = int(len([i for i in range(1, len(hour_group)) if hour_group[i - 1]['value'] < hour_group[i]['value']])
                   / len(hour_group) * 100)

        return rise, fall

    def __grouped_by_hours_interval(self, data: list, hours: int):
        data = [dict(datapoint, hour_group=self.__get_hour_group(datapoint['date'], hours)) for datapoint in data]
        sorted_by_date = sorted(data, key=lambda datapoint: datapoint['hour_group'])

        return [
                 list(datapoint)
                    for key, datapoint in itertools.groupby(sorted_by_date, key=lambda datapoint: datapoint['hour_group'])
                ]

    def __get_hour_group(self, date: str, hours: int):
        hour = datetime.strptime(date, '%m-%d %H:%M').hour

        return math.floor(hour / hours)