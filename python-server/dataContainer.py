import memcache
import json

class dataContainer:
    def __init__(self, clientString):
        self.client = memcache.Client([clientString])
        actuators = {'door' : False, 'window' :False, 'livingLight' : False, 'bedroomLight' : False}
        sensors = {'humidity' : 0, 'temperature' : 0, 'light' : 0, 'rain' : 0}
        self.keys = {'actuators' : actuators, 'sensors' : sensors}

    def __get(self, key):
        result = self.client.get(key)
        if (not result):
            return self.keys[key]

        return json.loads(result)

    def __set(self, key, name, value):
        actuators = self.__get(key)
        actuators[name] = value
        self.client.set(key, json.dumps(actuators))

    def getActuators(self):
        return self.__get('actuators')

    def setActuator(self, name, value):
        return self.__set('actuators', name, value)

    def getSensors(self):
        return self.__get('sensors')

    def setSensor(self, name, value):
        return self.__set('sensors', name, value)

