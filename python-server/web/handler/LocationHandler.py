from pydispatch import dispatcher

from event.LocationEvent import LocationEvent
from web.handler.BaseHandler import BaseHandler
from web.security.secure import secure


class LocationHandler(BaseHandler):
    @secure
    def post(self):
        latitude = float(self.get_argument('latitude', None, True))
        longitude = float(self.get_argument('longitude', None, True))
        username = self.get_argument('username', None, True)
        dispatcher.send(LocationEvent.NAME, event=LocationEvent(username, latitude, longitude))