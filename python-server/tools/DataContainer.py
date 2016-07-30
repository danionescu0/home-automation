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
        self.__add_sensors_in_history(name, value)

    def __add_sensors_in_history(self, name, value):
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

    def get_sensor_values_in_interval(self, startDate, endDate, groupByHours = None):
        startTimestamp = calendar.timegm(startDate.timetuple())
        endTimestamp = calendar.timegm(endDate.timetuple())
        range = self.client.zrangebyscore(self.sensors_history_key, startTimestamp, endTimestamp, withscores=True)
        for index, element in enumerate(range):
            timestamp = range[index][1]
            range[index] = json.loads(range[index][0])
            range[index]['timestamp'] = timestamp
        if groupByHours is None:
            return range
        lastHour = datetime.fromtimestamp(int(range[0]['timestamp'])).hour
        counter = 0
        averageData = range[0]
        groupedRange = []
        for datapoint in range:
            extractedHour = datetime.fromtimestamp(int(datapoint['timestamp'])).hour
            counter += 1
            if extractedHour != lastHour:
                lastHour = extractedHour
                averageData.update((x, y/counter) for x, y in averageData.items())
                groupedRange.append(averageData)
                counter = 0
            else:
                averageData = dict(Counter(averageData) + Counter(datapoint))

        return groupedRange
