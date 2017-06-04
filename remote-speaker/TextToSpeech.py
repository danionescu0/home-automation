import subprocess

class TextToSpeech:
    def __init__(self, chip):
        self.__chip = chip

    def say(self, text, nr_times = 1):
        self.__run_fix()
        [self.__say_once(text) for i in range(0, nr_times)]

    def __say_once(self, text):
        echo = subprocess.Popen(['echo', '"' + text + '"'],
                               stdout=subprocess.PIPE,
                               )
        festival = subprocess.Popen(["festival", "--tts"], stdin=echo.stdout, stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        festival.communicate()

    def __run_fix(self):
        if self.__chip == False:
            return
        self.__say_once("abc")