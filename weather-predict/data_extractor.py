from datetime import datetime, timedelta
import sys
import pandas
import requests
import statistics

url = "http://ip:8080/api/sensor/{0}?start_date={1}&end_date={2}"
sensors = ['humidity_outside', 'airPressure_outside', 'temperature_outside', 'rain_outside', 'light_outside']


class Extractor():
    def __init__(self, url: str, sensors: list) -> None:
        self.__url = url
        self.__sensors = sensors

    def get_for(self, date: datetime):
        useful_data = {}
        for sensor in self.__sensors:
            literal_date = date.strftime('%m-%d-%Y')
            request = self.__url.format(sensor, literal_date, literal_date)
            response = requests.get(request)
            data = response.json()['data']
            if not len(data):
                continue
            useful_data[sensor + '_min'] = min(datapoint['value'] for datapoint in data)
            useful_data[sensor + '_max'] = max(datapoint['value'] for datapoint in data)
            useful_data[sensor + '_mean'] = statistics.mean(datapoint['value'] for datapoint in data)
            useful_data['date'] = literal_date

        return useful_data


file_name = sys.argv[1]
days_behind = int(sys.argv[2])
extractor = Extractor(url, sensors)

extracted_data = []
for day_behind in range(days_behind, 0, -1):
    start_date = datetime.today() - timedelta(days=day_behind)
    extracted_data.append(extractor.get_for(start_date))
    print('Calculating day: ' + start_date.strftime('%m-%d-%Y'))


dataframe = pandas.DataFrame(extracted_data).set_index('date')
print(dataframe.describe().T)

print('Writing csv file with name:' + file_name)
dataframe.to_csv(file_name, sep=',')