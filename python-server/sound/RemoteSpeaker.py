import subprocess
from sound.SoundApi import SoundApi

from typeguard import typechecked

class TextToSpeech(SoundApi):
    @typechecked()
    def say(self, text: str, nr_times = 1) -> None:
        [self.__say_once(text) for i in range(0, nr_times)]

    def __say_once(self, text):
        echo = subprocess.Popen(['echo', '"' + text + '"'],
                               stdout=subprocess.PIPE,
                               )
        festival = subprocess.Popen(["festival", "--tts"], stdin=echo.stdout, stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        festival.communicate()