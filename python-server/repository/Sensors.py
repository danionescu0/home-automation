import calendar
import json
import math
from collections import Counter
from datetime import datetime

from repository.AbstractRedis import AbstractRedis

class Sensors(AbstractRedis):
    REDIS_SENSORS_KEY = 'sensors'
    REDIS_SENSORS_HISTORY_KEY = 'sensors_history_key'
    SENSORS_UPDATE_INTERVAL_IN_HISTORY = 300

    def __init__(self, redis_configuration):
        AbstractRedis.__init__(self, redis_configuration)
        sensors = {'humidity': 0, 'temperature': 0, 'light': 0, 'rain': 0, 'presence': 0, 'airQuality': 0,
                   'fingerprint': -1}
        self.keys = {self.REDIS_SENSORS_HISTORY_KEY: sensors}
        self.sensors_last_updated = 0
        self.last_averages = {}

    def get_sensors(self):
        return self.get(self.REDIS_SENSORS_KEY)

    def set_sensor(self, name, value):
        self.__set(self.REDIS_SENSORS_KEY, name, value)
        self.__add_last_sensor_averages_in_history(name, value)

    def __set(self, key, name, value):
        data = self.get(key)
        data[name] = value
        self.client.set(key, json.dumps(data))

    def __add_last_sensor_averages_in_history(self, name, value):
        if name not in self.last_averages.keys():
            self.last_averages[name] = []
        self.last_averages[name].append(value)
        currentTimestamp = calendar.timegm(datetime.now().timetuple())
        if (currentTimestamp - self.sensors_last_updated < self.SENSORS_UPDATE_INTERVAL_IN_HISTORY):
            return

        self.sensors_last_updated = currentTimestamp
        sensorsData = {}
        for key, list in self.last_averages.iteritems():
            sensorsData[key] = int(math.ceil(float(sum(list)) / len(list)))
        self.add_to_list(self.REDIS_SENSORS_HISTORY_KEY, sensorsData, None)
        self.last_averages = {}

    def get_sensor_values_in_interval(self, start_date, end_date):
        start_timestamp = calendar.timegm(start_date.timetuple())
        end_timestamp = calendar.timegm(end_date.timetuple())
        range = self.client.zrangebyscore(self.REDIS_SENSORS_HISTORY_KEY, start_timestamp, end_timestamp, withscores=True)
        for index, element in enumerate(range):
            timestamp = range[index][1]
            range[index] = json.loads(range[index][0])
            range[index]['timestamp'] = timestamp

        return range

    def get_hourly_sensor_values_in_interval(self, start_date, end_date):
        range = self.get_sensor_values_in_interval(start_date, end_date)
        last_hour = datetime.fromtimestamp(int(range[0]['timestamp'])).hour
        counter = 0
        average_date = range[0]
        grouped_range = []
        for datapoint in range:
            extracted_hour = datetime.fromtimestamp(int(datapoint['timestamp'])).hour
            counter += 1
            if extracted_hour != last_hour:
                last_hour = extracted_hour
                average_date.update((x, y / counter) for x, y in average_date.items())
                grouped_range.append(average_date)
                counter = 0
            else:
                average_date = dict(Counter(average_date) + Counter(datapoint))

        return grouped_range