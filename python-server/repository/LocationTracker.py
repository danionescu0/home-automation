import json
from typeguard import typechecked

from repository.AbstractRepository import AbstractRepository

class LocationTracker(AbstractRepository):
    @typechecked()
    def __init__(self, configuration: dict):
        AbstractRepository.__init__(self, configuration)
        self.location_key = 'location'

    @typechecked()
    def set(self, key: str, name: str, value) -> None:
        data = self.get(key)
        data[name]['state'] = value
        self.client.set(key, json.dumps(data))

    @typechecked()
    def add_location_point(self, username: str, latitude: float, longitude: float) -> None:
        data = {
            'username' : username,
            'lat' : latitude,
            'lng' : longitude
        }
        self.add_to_list(self.location_key, data)