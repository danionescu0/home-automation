import json

from typeguard import typechecked

from repository.ConfigurationRepository import ConfigurationRepository
from web.formatter.ConfigurationFormatter import ConfigurationFormatter
from web.factory.ConfigurationFactory import ConfigurationFactory
from web.handler.CorsHandler import CorsHandler
from web.security.secure import secure


class ConfigurationHandler(CorsHandler):
    @typechecked()
    def initialize(self, configuration_formatter: ConfigurationFormatter, configuration_factory: ConfigurationFactory,
                   configuration_repository: ConfigurationRepository):
        self.__configuration_formatter = configuration_formatter
        self.__configuration_factory = configuration_factory
        self.__configuration_repository = configuration_repository

    @secure
    def get(self):
        self.write(json.dumps(self.__configuration_formatter.get_all()))

    @secure
    def post(self):
        request_data = json.loads(self.request.body.decode("utf-8"))
        try:
            config_objects = self.__configuration_factory.from_request_data(request_data)
            self.__configuration_repository.set_all(config_objects)
            self.set_status(200)
        except Exception as e:
            print(e)
            self.set_status(500)
