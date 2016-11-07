from repository.IftttRules import IftttRules
import pprint

class CommandExecutor:
    def __init__(self, change_actuator_request_event, text_to_speech, logging):
        self.__change_actuator_request_event = change_actuator_request_event
        self.__text_to_speech = text_to_speech
        self.__logging = logging

    def execute(self, command):
        pprint.pprint(command)
        if command[IftttRules.COMMAND_VOICE] != '':
            self.__text_to_speech.say(command[IftttRules.COMMAND_VOICE])
        if command[IftttRules.COMMAND_ACTUATOR_NAME] != '':
            actuator_name = command[IftttRules.COMMAND_ACTUATOR_NAME]
            actuator_state = command[IftttRules.COMMAND_ACTUATOR_STATE]
            self.__logging.debug('Changing actuator {0} to state {1}'.format(actuator_name, actuator_state))
            self.__change_actuator_request_event.send(actuator_name, actuator_state)