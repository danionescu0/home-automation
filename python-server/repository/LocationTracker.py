import json

from repository.AbstractRedis import AbstractRedis

class LocationTracker(AbstractRedis):
    def __init__(self, configuration):
        AbstractRedis.__init__(self, configuration)
        self.locationKey = 'location'

    def set(self, key, name, value):
        data = self.get(key)
        if (key == self.sensorsKey):
            data[name] = value
        else:
            data[name]['state'] = value
        self.client.set(key, json.dumps(data))

    def add_location_point(self, deviceName, latitude, longitude):
        data = {
            'device' : deviceName,
            'lat' : latitude,
            'lng' : longitude
        }
        self.add_to_list(self.locationKey, data, None)