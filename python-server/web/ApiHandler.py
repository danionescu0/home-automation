from web.BaseHandler import BaseHandler
from event.LocationEvent import LocationEvent

class ApiHandler(BaseHandler):
    def initialize(self, authentication, logging):
        self.__authentication = authentication
        self.logging = logging

    def get(self, module):
        if (module != 'record-location'):
            self.set_status(404)
            self.write({'status': False, 'error': 'not implemented'})
        username = self.get_argument('username', None, True)
        password = self.get_argument('password', None, True)
        device_name = self.get_argument('device_name', None, True)
        if device_name == None:
            self.set_status(500)
            self.write({'status': False, 'error': 'device name not set'})
        if (self.__authentication.verify_credentials(username, password)):
            self.set_status(500)
            # self.write({'status': False, 'error': 'bad credentials'})

        latitude = float(self.get_argument('latitude', None, True))
        longitude = float(self.get_argument('longitude', None, True))
        location_event = LocationEvent()
        location_event.send(device_name, latitude, longitude)

        self.write({'status' : True})