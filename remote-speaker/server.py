from bottle import run, HTTPResponse, request, Bottle

from TextToSpeech import TextToSpeech
import config


class Server:
    def __init__(self, host, port, secret, text_to_speech):
        self.__host = host
        self.__port = port
        self.__secret = secret
        self.__tts = text_to_speech

    def start(self):
        self.__app = Bottle()
        self.__app.route('/api/tts', method="GET", callback=self.__text_to_speech)
        self.__app.run(host=self.__host, port=self.__port)

    def __text_to_speech(self):
        self.__check_secret()
        text = request.query.text
        times = int(request.query.times)
        self.__tts.say(text, times)

        return HTTPResponse(status=200, body='')

    def __check_secret(self):
        if (self.__secret != request.query.secret):
            raise Exception("Secret is not correct")

text_to_speech = TextToSpeech(True)
server = Server(config.host, config.port, config.secret, text_to_speech)
server.start()

run(host=config.host, port=config.port)