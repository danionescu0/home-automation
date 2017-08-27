from logging import RootLogger

from typeguard import typechecked
from event.ChangeActuatorRequestEvent import ChangeActuatorRequestEvent
from repository.IftttRules import IftttRules
from sound.SoundApi import SoundApi
from ifttt.command.TextCommunicationEnhancer import TextCommunicationEnhancer


class CommandExecutor:
    @typechecked()
    def __init__(self, change_actuator_request_event: ChangeActuatorRequestEvent,
                 text_communication_enhancer: TextCommunicationEnhancer,
                 sound_api : SoundApi, logging: RootLogger):
        self.__change_actuator_request_event = change_actuator_request_event
        self.__text_communication_enhancer = text_communication_enhancer
        self.__sound_api = sound_api
        self.__logging = logging

    @typechecked()
    def execute(self, command: dict) -> None:
        if command[IftttRules.COMMAND_VOICE] != '':
            enhanced_text = self.__text_communication_enhancer.enhance(command[IftttRules.COMMAND_VOICE])
            self.__sound_api.say(enhanced_text)
            self.__logging.debug('Speaking text: {0}'.format(command[IftttRules.COMMAND_VOICE]))
        if command[IftttRules.COMMAND_ACTUATOR_NAME] != '':
            actuator_name = command[IftttRules.COMMAND_ACTUATOR_NAME]
            actuator_state = command[IftttRules.COMMAND_ACTUATOR_STATE]
            self.__logging.debug('Changing actuator {0} to state {1}'.format(actuator_name, actuator_state))
            self.__change_actuator_request_event.send(actuator_name, actuator_state)