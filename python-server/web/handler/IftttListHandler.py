import json

from typeguard import typechecked

from web.formatter.IftttFormatter import IftttFormatter
from web.handler.CorsHandler import CorsHandler
from web.security.secure import secure


class IftttListHandler(CorsHandler):
    @typechecked()
    def initialize(self, ifttt_formatter: IftttFormatter):
        self.__ifttt_formatter = ifttt_formatter

    @secure
    def get(self):
        self.write(json.dumps(self.__ifttt_formatter.get_all()))