import json
import redis
from datetime import datetime
import calendar
import random
import math
import collections

class dataContainer:
    def __init__(self, config):
        self.client = redis.StrictRedis(**config)
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
            'powerSocket1' : {'state' : False, 'type': 'bi', 'device' : 'powerSocket'},
            'livingCourtains' : {'state' : False, 'type': 'bi', 'device' : 'livingCourtains'},
        }
        sensors = {'humidity' : 0, 'temperature' : 0, 'light' : 0, 'rain' : 0, 'presence' : 0, 'airQuality' : 0}
        self.sensorsLastUpdated = 0
        self.keys = {'actuators' : actuators, 'sensors' : sensors, 'time_rules': {}}
        self.updateThresholdSeconds = 300
        self.sensorsHistoryKey = 'sensors_history_key'
        self.sensorsKey = 'sensors'
        self.timeRules = 'time_rules'
        self.lastAverages = {}

    def __get(self, key):
        result = self.client.get(key)
        if (not result):
            return self.keys[key]

        return json.loads(result)

    def __set(self, key, name, value):
        data = self.__get(key)
        if (key == self.sensorsKey):
            data[name] = value
        else:
            data[name]['state'] = value
        self.client.set(key, json.dumps(data))

    def getActuators(self, justNames = False):
        if not justNames:
            actuators = self.__get('actuators')
            return collections.OrderedDict(sorted(actuators.items()))

        actuators = self.__get('actuators')
        actuatorNames = []
        for name, data in actuators.iteritems():
            actuatorNames.append(name)

        return actuatorNames

    def setActuator(self, name, value):
        return self.__set('actuators', name, value)

    def getSensors(self):
        return self.__get(self.sensorsKey)

    def setSensor(self, name, value):
        self.__set(self.sensorsKey, name, value)
        self.__addSensorsInHistory(name, value)

    def upsertTimeRule(self, name, actuator, state, time, active):
        rules = self.__get(self.timeRules)
        rules[name] = {
            'actuator' : actuator,
            'state' : state,
            'active': active,
            'time' : time.isoformat()
        }

        return self.client.set(self.timeRules, json.dumps(rules))

    def deleteTimeRule(self, name):
        rules = self.__get(self.timeRules)
        rules.pop(name, None)

        return self.client.set(self.timeRules, json.dumps(rules))


    def getTimeRules(self):
        rules = self.__get(self.timeRules)
        print rules
        print "jb"
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
        sensorsData["randomize"] = random.randint(0, 999999999)
        self.client.zadd(self.sensorsHistoryKey, currentTimestamp, json.dumps(sensorsData))
        self.lastAverages = {}

    def getSensorValuesInInterval(self, startDate, endDate):
        startTimestamp = calendar.timegm(startDate.timetuple())
        endTimestamp = calendar.timegm(endDate.timetuple())
        range = self.client.zrangebyscore(self.sensorsHistoryKey, startTimestamp, endTimestamp, withscores=True)
        for index, element in enumerate(range):
            timestamp = range[index][1]
            range[index] = json.loads(range[index][0])
            range[index]['timestamp'] = timestamp

        return range

