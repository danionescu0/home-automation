from event.LocationEvent import LocationEvent
from web.BaseHandler import BaseHandler
from web.security.secure import secure

class ApiLocationHandler(BaseHandler):
    @secure
    def post(self):
        latitude = float(self.get_argument('latitude', None, True))
        longitude = float(self.get_argument('longitude', None, True))
        username = self.get_argument('username', None, True)
        location_event = LocationEvent()
        location_event.send(username, latitude, longitude)