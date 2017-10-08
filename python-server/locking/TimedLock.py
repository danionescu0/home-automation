import redis

from typeguard import typechecked


class TimedLock:
    @typechecked()
    def __init__(self, configuration: dict):
        self.__configuration = configuration
        self.client = None

    @typechecked()
    def set_lock(self, key: str, seconds: int) -> None:
        self.__get_client().set(key, "1", ex = seconds)

    def has_lock(self, key: str) -> bool:
        if None == self.__get_client().get(key):
            return False

        return True

    def __get_client(self):
        if (None != self.client):
            return self.client

        self.client = redis.StrictRedis(**self.__configuration)

        return self.client