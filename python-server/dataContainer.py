import json
from datetime import datetime
import calendar
import random
import math
import collections
from collections import Counter
from abstractRedis import abstractRedis

class dataContainer(abstractRedis):
    def __init__(self, config):
        abstractRedis.__init__(self, config)
        actuators = {
            'door' : {'state' : False, 'type': 'single', 'device': 'door'},
            'homeAlarm' : {'state' : False, 'type': 'bi', 'device': 'action'},
            'window' : {'state' : False, 'type': 'bi', 'device' : 'window'},
            'windowNodgeDown' : {'state' : False, 'type': 'single', 'device' : 'window'},
            'closeAllLights' : {'state' : False, 'type': 'single', 'device': 'action'},
            'livingLight' : {'state' : False, 'type': 'bi', 'device' : 'light'},
            'bedroomLight' : {'state' : False, 'type': 'bi', 'device' : 'light'},
            'kitchenLight' : {'state' : False, 'type': 'bi', 'device' : 'light'},
            'holwayLight' : {'state' : False, 'type': 'bi', 'device' : 'light'},
            'closetLight' : {'state' : False, 'type': 'bi', 'device' : 'light'},
            'balconyLight' : {'state' : False, 'type': 'bi', 'device' : 'light'},
            'powerSocket1' : {'state' : False, 'type': 'bi', 'device' : 'powerSocket'},
            'livingCourtains' : {'state' : False, 'type': 'bi', 'device' : 'livingCourtains'},
        }
        sensors = {'humidity' : 0, 'temperature' : 0, 'light' : 0, 'rain' : 0, 'presence' : 0, 'airQuality' : 0,
                    'fingerprint' : -1}
        self.keys = {'actuators' : actuators, 'sensors' : sensors, 'time_rules': {}}

        self.sensorsLastUpdated = 0
        self.updateThresholdSeconds = 300
        self.sensorsHistoryKey = 'sensors_history_key'
        self.sensorsKey = 'sensors'
        self.timeRules = 'time_rules'
        self.locationKey = 'location'
        self.actuatorsKey = 'actuators'
        self.lastAverages = {}

    def get(self, key):
        result = self.client.get(key)
        if (not result):
            return self.keys[key]

        return json.loads(result)

    def set(self, key, name, value):
        data = self.get(key)
        if (key == self.sensorsKey):
            data[name] = value
        else:
            data[name]['state'] = value
        self.client.set(key, json.dumps(data))

    def getActuators(self, justNames = False):
        if not justNames:
            actuators = self.get(self.actuatorsKey)
            return collections.OrderedDict(sorted(actuators.items()))

        actuators = self.get(self.actuatorsKey)
        actuatorNames = []
        for name, data in actuators.iteritems():
            actuatorNames.append(name)

        return actuatorNames

    def setActuator(self, name, value):
        return self.set(self.actuatorsKey, name, value)

    def getSensors(self):
        return self.get(self.sensorsKey)

    def setSensor(self, name, value):
        self.set(self.sensorsKey, name, value)
        self.__addSensorsInHistory(name, value)

    def upsertTimeRule(self, name, actuator, state, time, active):
        rules = self.get(self.timeRules)
        rules[name] = {
            'actuator' : actuator,
            'state' : state,
            'active': active,
            'time' : time.isoformat()
        }

        return self.client.set(self.timeRules, json.dumps(rules))

    def deleteTimeRule(self, name):
        rules = self.get(self.timeRules)
        rules.pop(name, None)

        return self.client.set(self.timeRules, json.dumps(rules))

    def getTimeRules(self):
        rules = self.get(self.timeRules)
        for rule in rules:
            rules[rule]['stringTime'] = rules[rule]['time']
            rules[rule]['time'] = datetime.strptime(rules[rule]['time'], "%H:%M:%S").time()

        return rules

    def __addSensorsInHistory(self, name, value):
        if name not in self.lastAverages.keys():
            self.lastAverages[name] = []
        self.lastAverages[name].append(value)
        currentTimestamp = calendar.timegm(datetime.now().timetuple())
        if (currentTimestamp - self.sensorsLastUpdated < self.updateThresholdSeconds):
            return

        self.sensorsLastUpdated = currentTimestamp
        sensorsData = {}
        for key, list in self.lastAverages.iteritems():
            sensorsData[key] = int(math.ceil(float(sum(list)) / len(list)))
        self.addToList(self.sensorsHistoryKey, sensorsData, None)
        self.lastAverages = {}

    def getSensorValuesInInterval(self, startDate, endDate, groupByHours = None):
        startTimestamp = calendar.timegm(startDate.timetuple())
        endTimestamp = calendar.timegm(endDate.timetuple())
        range = self.client.zrangebyscore(self.sensorsHistoryKey, startTimestamp, endTimestamp, withscores=True)
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
