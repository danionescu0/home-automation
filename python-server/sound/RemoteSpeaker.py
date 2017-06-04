from sound.SoundApi import SoundApi
import requests
import urllib
from typeguard import typechecked

class RemoteSpeaker(SoundApi):
    SAY_URL = '{0}/api/tts'

    def __init__(self, host, secret) -> None:
        self.__host = host
        self.__secret = secret

    @typechecked()
    def say(self, text: str, nr_times = 1) -> bool:
        params = (('text', text), ('times', nr_times), ('secret', self.__secret))
        say_url = self.__get_say_url() + "?" + urllib.parse.urlencode(params)
        try:
            requests.get(say_url, timeout = 1)
        except Exception:
            return False

        return True

    def __get_say_url(self):
        return self.SAY_URL.format(self.__host)
