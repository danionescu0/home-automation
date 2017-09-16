from typeguard import typechecked

from event.LocationEvent import LocationEvent
from web.BaseHandler import BaseHandler


class ApiLocationHandler(BaseHandler):
    @typechecked()
    def initialize(self, api_token_secret: str):
        self.api_token_secret = api_token_secret

    def post(self):
        username = self.check_token()
        if not username:
            return False
        latitude = float(self.get_argument('latitude', None, True))
        longitude = float(self.get_argument('longitude', None, True))
        location_event = LocationEvent()
        location_event.send(username, latitude, longitude)
        print('send location')
        print(latitude)
        self.write({'status': True})