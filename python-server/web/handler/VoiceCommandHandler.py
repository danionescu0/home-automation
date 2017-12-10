from typeguard import typechecked

from tools.VoiceCommands import VoiceCommands
from web.handler.BaseHandler import BaseHandler
from web.security.secure import secure


class VoiceCommandHandler(BaseHandler):
    @typechecked()
    def initialize(self, voice_commands: VoiceCommands):
        self.__voice_commands = voice_commands

    @secure
    def post(self):
        command = self.get_argument('command', None, True)
        self.__voice_commands.execute(command)