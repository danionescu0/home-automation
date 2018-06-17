import sys
import pandas
import requests
import statistics
import itertools
import math
from datetime import datetime, timedelta
import pprint

import config


class Extractor():
    def __init__(self, url: str, sensors: list) -> None:
        self.__url = url
        self.__sensors = sensors

    def get_for(self, date: datetime):
        useful_data = []
        for sensor in self.__sensors:
            literal_date = date.strftime('%m-%d-%Y')
            request = self.__url.format(sensor, literal_date, literal_date)
            response = requests.get(request)
            data = response.json()['data']
            if not len(data):
                continue
            grouped_by_hour = self.__grouped_by_hours_interval(data, 6)
            for hour_data in grouped_by_hour:
                last_group = {}
                last_group['date'] = literal_date + ' ' + str(hour_data[0]['hour_group'])
                last_group['hour_group'] = hour_data[0]['hour_group']
                last_group[sensor + '_min'] = min(datapoint['value'] for datapoint in hour_data)
                last_group[sensor + '_max'] = max(datapoint['value'] for datapoint in hour_data)
                last_group[sensor + '_mean'] = statistics.mean(datapoint['value'] for datapoint in hour_data)
                useful_data.append(last_group)

        last_process = {}
        for datapoint in useful_data:
            if not datapoint['date'] in last_process:
                last_process[datapoint['date']] = datapoint
            last_process[datapoint['date']].update(datapoint)

        as_list = [value for key, value in last_process.items()]

        return sorted(as_list, key=lambda datapoint: datapoint['hour_group'])

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


file_name = sys.argv[1]
days_behind = int(sys.argv[2])
extractor = Extractor(config.url, config.sensors)

extracted_data = []
for day_behind in range(days_behind, 0, -1):
    start_date = datetime.today() - timedelta(days=day_behind)
    extracted_data = extracted_data + extractor.get_for(start_date)
    print('Calculating day: ' + start_date.strftime('%m-%d-%Y'))

pprint.pprint(extracted_data)
dataframe = pandas.DataFrame(extracted_data).set_index('date')
print(dataframe.describe().T)

print('Writing csv file with name:' + file_name)
dataframe.to_csv(file_name, sep=',')