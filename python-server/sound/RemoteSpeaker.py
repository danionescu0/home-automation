import requests
import urllib
from typeguard import typechecked

from sound.SoundApi import SoundApi

class RemoteSpeaker(SoundApi):
    SAY_URL = '{0}/api/tts'

    def __init__(self, host, user, password) -> None:
        self.__host = host
        self.__user = user
        self.__password = password

    @typechecked()
    def say(self, text: str, nr_times = 1) -> bool:
        params = (('text', text), ('times', nr_times))
        say_url = self.__get_say_url() + "?" + urllib.parse.urlencode(params)
        try:
            requests.get(say_url, timeout = 1, auth=(self.__user, self.__password))
        except Exception:
            return False

        return True

    def __get_say_url(self):
        return self.SAY_URL.format(self.__host)