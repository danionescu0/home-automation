import json

from repository.AbstractRedis import AbstractRedis

class LocationTracker(AbstractRedis):
    def __init__(self, configuration):
        AbstractRedis.__init__(self, configuration)
        self.location_key = 'location'

    def set(self, key, name, value):
        data = self.get(key)
        if (key == self.sensorsKey):
            data[name] = value
        else:
            data[name]['state'] = value
        self.client.set(key, json.dumps(data))

    def add_location_point(self, username, latitude, longitude):
        data = {
            'username' : username,
            'lat' : latitude,
            'lng' : longitude
        }
        self.add_to_list(self.location_key, data, None)