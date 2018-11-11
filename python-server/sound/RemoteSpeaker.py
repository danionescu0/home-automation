import requests
import urllib
from typeguard import typechecked

from sound.SoundApi import SoundApi
from model.configuration.RemoteSpeakerCfg import RemoteSpeakerCfg


class RemoteSpeaker(SoundApi):
    SAY_URL = '{0}/api/tts'

    def __init__(self, remote_speaker_cfg: RemoteSpeakerCfg) -> None:
        self.__remote_speaker_cfg = remote_speaker_cfg

    @typechecked()
    def say(self, text: str, nr_times = 1) -> bool:
        params = (('text', text), ('times', nr_times))
        say_url = self.__get_say_url() + "?" + urllib.parse.urlencode(params)
        try:
            requests.get(say_url, timeout = 1, auth=(self.__remote_speaker_cfg.user, self.__remote_speaker_cfg.password))
        except Exception:
            return False

        return True

    def __get_say_url(self):
        return self.SAY_URL.format(self.__remote_speaker_cfg.host)