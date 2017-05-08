import subprocess
from typeguard import typechecked

class TextToSpeech:
    @typechecked()
    def say(self, text: str, nr_times = 1) -> None:
        for i in range(0, nr_times):
            self.__say_once(text)

    def __say_once(self, text):
        echo = subprocess.Popen(['echo', '"' + text + '"'],
                               stdout=subprocess.PIPE,
                               )
        festival = subprocess.Popen(["festival", "--tts"], stdin=echo.stdout, stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        festival.communicate()