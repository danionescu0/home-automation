import re

from adapt.intent import IntentBuilder
from adapt.engine import IntentDeterminationEngine

class VoiceCommands:
    ACTIONS = 'Action'
    NAME = 'Name'
    ACTUATOR_TYPE = 'ActuatorType'

    def __init__(self, job_controll, logging):
        self.__job_controll = job_controll
        self.__logging = logging

    def configure(self):
        self.__engine = IntentDeterminationEngine()
        actions = ['on', 'off']
        self.__register_entity(actions, self.ACTIONS)
        locations = ['living', 'kitchen', 'hollway', 'wemo']
        self.__register_entity(locations, self.NAME)
        actuator_types = ['light', 'switch', 'courtains', 'door']
        self.__register_entity(actuator_types, self.ACTUATOR_TYPE)

        actuator_intent = IntentBuilder("ActuatorIntent") \
            .require(self.ACTIONS) \
            .require(self.ACTUATOR_TYPE) \
            .require(self.NAME) \
            .build()
        self.__engine.register_intent_parser(actuator_intent)
        self.__commands_map = [
            {'entities' : {'name' : 'living', 'type' : 'light'}, 'actuator' : 'livingLight'},
            {'entities' : {'name' : 'living', 'type' : 'courtains'}, 'actuator' : 'livingCourtains'},
            {'entities' : {'name' : 'hollway', 'type' : 'light'}, 'actuator' : 'holwayLight'},
            {'entities' : {'name' : 'wemo', 'type' : 'switch'}, 'actuator' : 'wemoSwitch1'},
        ]

        return self

    def execute(self, command):
        command = self.__normalize_command(command)
        print command
        for intent in self.__engine.determine_intent(command):
            if intent and intent.get('confidence') > 0:
                self.__logging.debug(intent)
                command = self.__get_matching_command(intent)
                self.__run_command(command, intent)

    def __register_entity(self, wordlist, name):
        for action in wordlist:
            self.__engine.register_entity(action, name)

    def __get_matching_command(self, intent):
        for command in self.__commands_map:
            if command['entities']['name'] == intent[self.NAME] and \
                command['entities']['type'] == intent[self.ACTUATOR_TYPE]:
                return command

    def __run_command(self, command, intent):
        if None == command:
            return
        actuator_state = (False, True)[intent[self.ACTIONS] == 'on']
        self.__logging.debug('Changin actuator {0} value: {1}'.format(command['actuator'], actuator_state))
        self.__job_controll.change_actuator(command['actuator'], actuator_state)

    def __normalize_command(self, command):
        # replaces = [('life', 'light'), ('leaving', 'living'), ('hallway', 'hollway'), ('quarters', 'courtains'), ('of', 'off')]
        replaces = [('life', 'light'), ('leaving', 'living'), ('hallway', 'hollway'), ('quarters', 'courtains')]
        for replace in replaces:
            command = re.sub(replace[0], replace[1], command)

        return command