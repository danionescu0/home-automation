import json

from AbstractRedis import abstractRedis

class LocationTracker(abstractRedis):
    def __init__(self, config):
        abstractRedis.__init__(self, config)
        self.locationKey = 'location'

    def set(self, key, name, value):
        data = self.get(key)
        if (key == self.sensorsKey):
            data[name] = value
        else:
            data[name]['state'] = value
        self.client.set(key, json.dumps(data))

    def addLocationPoint(self, deviceName, latitude, longitude):
        data = {
            'device' : deviceName,
            'lat' : latitude,
            'lng' : longitude
        }
        self.addToList(self.locationKey, data, None)