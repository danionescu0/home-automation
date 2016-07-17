from web.BaseHandler import BaseHandler
from event.Location import Location

class ApiHandler(BaseHandler):
    def initialize(self, data_container, credentials, logging):
        self.data_container = data_container
        self.credentials = credentials
        self.logging = logging

    def get(self, module):
        if (module != 'record-location'):
            self.set_status(404)
            self.write({'status': False, 'error': 'not implemented'})
        username = self.get_argument('username', None, True)
        password = self.get_argument('password', None, True)
        deviceName = self.get_argument('device_name', None, True)
        if deviceName == None:
            self.set_status(500)
            self.write({'status': False, 'error': 'device name not set'})
        if (username != self.credentials['username'] or password != self.credentials['password']):
            self.set_status(500)
            self.write({'status': False, 'error': 'bad credentials'})

        latitude = float(self.get_argument('latitude', None, True))
        longitude = float(self.get_argument('longitude', None, True))
        locationEvent = Location()
        locationEvent.send(deviceName, latitude, longitude)

        self.write({'status' : True})