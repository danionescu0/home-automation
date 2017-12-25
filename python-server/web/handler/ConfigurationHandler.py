import json

from typeguard import typechecked

from web.formatter.ConfigurationFormatter import ConfigurationFormatter
from web.handler.CorsHandler import CorsHandler
from web.security.secure import secure


class ConfigurationHandler(CorsHandler):
    @typechecked()
    def initialize(self, configuration_formatter: ConfigurationFormatter):
        self.__configuration_formatter = configuration_formatter

    @secure
    def get(self):
        self.write(json.dumps(self.__configuration_formatter.get_all()))
