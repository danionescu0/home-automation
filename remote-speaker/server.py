from bottle import run, HTTPResponse, request, Bottle, auth_basic, parse_auth

from TextToSpeech import TextToSpeech
import config

class Server:
    def __init__(self, config, text_to_speech):
        self.__config = config
        self.__tts = text_to_speech

    def start(self):
        self.__app = Bottle()
        self.__app.route('/api/tts', method="GET", callback=self.__text_to_speech)
        self.__app.run(host=self.__config.host, port=self.__config.port)

    def __text_to_speech(self):
        self.__check_auth()
        text = request.query.text
        times = int(request.query.times)
        self.__tts.say(text, times)

        return HTTPResponse(status=200, body='')

    def __check_auth(self):
        auth = request.headers.get('Authorization')
        credentials = parse_auth(auth)
        if self.__config.http_user != credentials[0] or self.__config.http_pass != credentials[1]:
            raise Exception('Request is not authorized')

text_to_speech = TextToSpeech(True)
server = Server(config, text_to_speech)
server.start()