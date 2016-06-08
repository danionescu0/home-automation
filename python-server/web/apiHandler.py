from web.baseHandler import baseHandler
from event.location import location

class apiHandler(baseHandler):
    def initialize(self, dataContainer, credentials, logging):
        self.dataContainer = dataContainer
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
        locationEvent = location()
        locationEvent.send(deviceName, latitude, longitude)

        self.write({'status' : True})