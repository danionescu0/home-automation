import jsonpickle

from typeguard import typechecked

from repository.AbstractRepository import AbstractRepository


class FeaturesConfigurationRepository(AbstractRepository):
    __REDIS_KEY = 'configuration_{0}'

    @typechecked()
    def __init__(self, configuration: dict):
        AbstractRepository.__init__(self, configuration)

    @typechecked()
    def get_config(self, name: object):
        return self.__get(name.__class__.__name__)

    @typechecked()
    def has(self, name: object):
        return True if self.__get(name.__class__.__name__) else False

    @typechecked()
    def set(self, name: object, model: object):
        return self.client.set(self.__get_key(name.__class__.__name__), jsonpickle.encode(model))

    def __get(self, name):
        config = self.client.get(self.__get_key(name))
        if config:
            return jsonpickle.decode(config.decode("utf-8"))

        return None

    def __get_key(self, name):
        return self.__REDIS_KEY.format(name)