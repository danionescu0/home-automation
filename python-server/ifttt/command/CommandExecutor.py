from logging import RootLogger

from pydispatch import dispatcher
from typeguard import typechecked
from sound.SoundApi import SoundApi
from tools.EmailNotifier import EmailNotifier
from ifttt.command.TextCommunicationEnhancer import TextCommunicationEnhancer
from model.RuleCommand import RuleCommand
from event.ChangeActuatorRequestEvent import ChangeActuatorRequestEvent


#@ToDo break this class when you need to add another rule type
#refactor rule command also
class CommandExecutor:
    @typechecked()
    def __init__(self, text_communication_enhancer: TextCommunicationEnhancer,
                 sound_api : SoundApi, email_notifier: EmailNotifier, logging: RootLogger):
        self.__text_communication_enhancer = text_communication_enhancer
        self.__sound_api = sound_api
        self.__email_notifier = email_notifier
        self.__logging = logging

    @typechecked()
    def execute(self, command: RuleCommand) -> None:
        if command.has_voice():
            enhanced_text = self.__text_communication_enhancer.enhance(command.voice_text)
            self.__sound_api.say(enhanced_text)
            self.__logging.info('Speaking text: {0}'.format(command.voice_text))
        if command.has_email():
            self.__logging.info('Sending email: {0}'.format(command.voice_text))
            enhanced_text = self.__text_communication_enhancer.enhance(command.email_text)
            self.__email_notifier.send_alert(
                "This is an configured email alert from HomeAutomation system", enhanced_text)
        if command.has_actuator():
            self.__logging.info('Changing actuator: {0} to new value: {1}'
                                 .format(command.actuator_id, command.actuator_state))
            dispatcher.send(ChangeActuatorRequestEvent.NAME,
                            event=ChangeActuatorRequestEvent(command.actuator_id, command.actuator_state))