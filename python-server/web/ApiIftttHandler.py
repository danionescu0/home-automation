import json

from typeguard import typechecked

from web.CorsHandler import CorsHandler
from web.security.secure import secure
from web.formatter.IftttFormatter import IftttFormatter


class ApiIftttHandler(CorsHandler):
    @typechecked()
    def initialize(self, ifttt_formatter: IftttFormatter):
        self.__ifttt_formatter = ifttt_formatter

    @secure
    def get(self):
        self.write(json.dumps(self.__ifttt_formatter.get_all()))