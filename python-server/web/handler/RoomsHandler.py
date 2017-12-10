import json

from typeguard import typechecked

from web.formatter.RoomsFormatter import RoomsFormatter
from web.handler.CorsHandler import CorsHandler
from web.security.secure import secure


class RoomsHandler(CorsHandler):
    @typechecked()
    def initialize(self, rooms_formatter: RoomsFormatter):
        self.__rooms_formatter = rooms_formatter

    @secure
    def get(self):
        self.write(json.dumps(self.__rooms_formatter.get_rooms()))