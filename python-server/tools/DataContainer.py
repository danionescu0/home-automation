import json
import calendar
import math
import collections
from collections import Counter
from AbstractRedis import AbstractRedis
from datetime import datetime

class DataContainer(AbstractRedis):
    def __init__(self, redis_configuration, actuators_config):
        AbstractRedis.__init__(self, redis_configuration)
        sensors = {'humidity' : 0, 'temperature' : 0, 'light' : 0, 'rain' : 0, 'presence' : 0, 'airQuality' : 0,
                    'fingerprint' : -1}
        self.keys = {'actuators' : actuators_config, 'sensors' : sensors}

        self.sensors_last_updated = 0
        self.update_threshold_seconds = 300
        self.sensors_history_key = 'sensors_history_key'
        self.sensors_key = 'sensors'
        self.actuators_key = 'actuators'
        self.last_averages = {}

    def __set(self, key, name, value):
        data = self.get(key)
        if (key == self.sensors_key):
            data[name] = value
        else:
            data[name]['state'] = value
        self.client.set(key, json.dumps(data))

    def get_actuators(self, justNames = False):
        if not justNames:
            actuators = self.get(self.actuators_key)
            return collections.OrderedDict(sorted(actuators.items()))

        actuators = self.get(self.actuators_key)
        actuatorNames = []
        for name, data in actuators.iteritems():
            actuatorNames.append(name)

        return actuatorNames

    def set_actuator(self, name, value):
        return self.__set(self.actuators_key, name, value)

    def get_sensors(self):
        return self.get(self.sensors_key)

    def set_sensor(self, name, value):
        self.__set(self.sensors_key, name, value)
        self.__add_last_sensor_averages_in_history(name, value)

    def __add_last_sensor_averages_in_history(self, name, value):
        if name not in self.last_averages.keys():
            self.last_averages[name] = []
        self.last_averages[name].append(value)
        currentTimestamp = calendar.timegm(datetime.now().timetuple())
        if (currentTimestamp - self.sensors_last_updated < self.update_threshold_seconds):
            return

        self.sensors_last_updated = currentTimestamp
        sensorsData = {}
        for key, list in self.last_averages.iteritems():
            sensorsData[key] = int(math.ceil(float(sum(list)) / len(list)))
        self.add_to_list(self.sensors_history_key, sensorsData, None)
        self.last_averages = {}

    def get_sensor_values_in_interval(self, start_date, end_date):
        start_timestamp = calendar.timegm(start_date.timetuple())
        end_timestamp = calendar.timegm(end_date.timetuple())
        range = self.client.zrangebyscore(self.sensors_history_key, start_timestamp, end_timestamp, withscores=True)
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