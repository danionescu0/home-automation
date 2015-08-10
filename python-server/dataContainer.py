import json
import redis
from datetime import datetime
import calendar
import random

class dataContainer:
    def __init__(self, config):
        self.client = redis.StrictRedis(**config)
        actuators = {
            'door' : {'state' : False, 'type': 'single'},
            'window' : {'state' : False, 'type': 'bi'},
            'livingLight' : {'state' : False, 'type': 'bi'},
            'bedroomLight' : {'state' : False, 'type': 'bi'},
            'kitchenLight' : {'state' : False, 'type': 'bi'},
            'holwayLight' : {'state' : False, 'type': 'bi'},
        }
        sensors = {'humidity' : 0, 'temperature' : 0, 'light' : 0, 'rain' : 0, 'presence' : 0}
        self.sensorsLastUpdated = 0
        self.keys = {'actuators' : actuators, 'sensors' : sensors, 'time_rules': {}}
        self.updateThresholdSeconds = 300
        self.sensorsHistoryKey = 'sensors_history_key'
        self.sensorsKey = 'sensors'
        self.timeRules = 'time_rules'

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

    def getActuators(self):
        return self.__get('actuators')

    def setActuator(self, name, value):
        return self.__set('actuators', name, value)

    def getSensors(self):
        return self.__get(self.sensorsKey)

    def setSensor(self, name, value):
        self.__set(self.sensorsKey, name, value)
        self.__addSensorsInHistory()

    def upsertTimeRule(self, name, actuator, state, time):
        rules = self.__get(self.timeRules)
        rules[name] = {
            'actuator' : actuator,
            'state' : state,
            'time' : time.isoformat()
        }

        return  self.client.set(self.timeRules, json.dumps(rules))

    def getTimeRules(self):
        rules = self.__get(self.timeRules)
        for rule in rules:
            rules[rule]['stringTime'] = rules[rule]['time']
            rules[rule]['time'] = datetime.strptime(rules[rule]['time'], "%H:%M:%S").time()

        return rules

    def __addSensorsInHistory(self):
        currentTimestamp = calendar.timegm(datetime.now().timetuple())
        if (currentTimestamp - self.sensorsLastUpdated < self.updateThresholdSeconds):
            return

        self.sensorsLastUpdated = currentTimestamp
        sensorsData = self.__get(self.sensorsKey)
        sensorsData["randomize"] = random.randint(0, 999999999)
        self.client.zadd(self.sensorsHistoryKey, currentTimestamp, json.dumps(sensorsData))

    def getSensorValuesInInterval(self, startDate, endDate):
        startTimestamp = calendar.timegm(startDate.timetuple())
        endTimestamp = calendar.timegm(endDate.timetuple())
        range = self.client.zrangebyscore(self.sensorsHistoryKey, startTimestamp, endTimestamp, withscores=True)
        for index, element in enumerate(range):
            timestamp = range[index][1]
            range[index] = json.loads(range[index][0])
            range[index]['timestamp'] = timestamp

        return range

