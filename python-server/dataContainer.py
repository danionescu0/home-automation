import json
import redis

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
        sensors = {'humidity' : 0, 'temperature' : 0, 'light' : 0, 'rain' : 0}
        self.keys = {'actuators' : actuators, 'sensors' : sensors}

    def __get(self, key):
        result = self.client.get(key)
        if (not result):
            return self.keys[key]

        return json.loads(result)

    def __set(self, key, name, value):
        data = self.__get(key)
        if (key == 'sensors'):
            data[name] = value
        else:
            data[name]['state'] = value
        self.client.set(key, json.dumps(data))

    def getActuators(self):
        return self.__get('actuators')

    def setActuator(self, name, value):
        return self.__set('actuators', name, value)

    def getSensors(self):
        return self.__get('sensors')

    def setSensor(self, name, value):
        return self.__set('sensors', name, value)

