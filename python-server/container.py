from typing import Callable
import sys

from config import actuators
from config import general
from config import sensors

from communication.CommunicatorRegistry import CommunicatorRegistry
from communication.TextSensorDataParser import TextSensorDataParser
from communication.actuator.ActuatorCommands import ActuatorCommands
from communication.actuator.ActuatorStrategiesBuilder import ActuatorStrategiesBuilder
from communication.encriptors.EncriptorsBuilder import EncriptorsBuilder

from event.ChangeActuatorRequestEvent import ChangeActuatorRequestEvent
from event.SensorUpdateEvent import SensorUpdateEvent
from ifttt.command.CommandExecutor import CommandExecutor
from ifttt.parser.Tokenizer import Tokenizer
from ifttt.command.TextCommunicationEnhancer import TextCommunicationEnhancer
from ifttt.ExpressionValidator import ExpressionValidator
from ifttt.parser.ActuatorTokenConverter import ActuatorTokenConverter
from ifttt.parser.SensorTokenConverter import SensorTokenConverter
from ifttt.parser.CurrentTimeTokenConverter import CurrentTimeTokenConverter
from ifttt.parser.ActuatorStateTokenConverter import ActuatorStateTokenConverter
from ifttt.parser.BooleanTokenConverter import BooleanTokenConverter
from ifttt.parser.IntTokenConverter import IntTokenConverter
from listener.ChangeActuatorListener import ChangeActuatorListener
from listener.FingerprintDoorUnlockListener import FingerprintDoorUnlockListener
from listener.IntruderAlertListener import IntruderAlertListener
from listener.SaveLocationListener import SaveLocationListener
from listener.SetPhoneIsHomeListener import SetPhoneIsHomeListener
from repository.ActuatorsRepository import ActuatorsRepository
from repository.IftttRulesRepository import IftttRulesRepository
from repository.SensorsRepository import SensorsRepository
from repository.LocationTrackerRepository import LocationTrackerRepository
from sound.RemoteSpeaker import RemoteSpeaker
from sound.SoundApi import SoundApi
from tools.Authentication import Authentication
from tools.EmailNotifier import EmailNotifier
from tools.HomeDefence import HomeDefence
from tools.AsyncJobs import AsyncJobs
from tools.LoggingConfig import LoggingConfig
from tools.VoiceCommands import VoiceCommands
from logging import RootLogger


def singleton(function: Callable):
    caching = {}
    def wrapper(*args, **kwargs):
        if function.__name__ in caching:
            return caching[function.__name__]
        caching[function.__name__] = function(*args, **kwargs)

        return caching[function.__name__]

    return wrapper


class Container:
    @singleton
    def root_logger(self) -> RootLogger:
        logging_config = LoggingConfig(general.logging['log_file'], general.logging['log_entries'])
        sys.excepthook = logging_config.set_error_hadler

        return logging_config.get_logger()

    @singleton
    def communicator_registry(self) -> CommunicatorRegistry:
        return CommunicatorRegistry(general.communication, self.root_logger())

    @singleton
    def sound_api(self) -> SoundApi:
        return  RemoteSpeaker(general.remote_speaker['host'], general.remote_speaker['user'],
                              general.remote_speaker['password'])

    @singleton
    def location_tracker_repository(self) -> LocationTrackerRepository:
        return LocationTrackerRepository(general.redis_config)

    @singleton
    def actuators_repository(self) -> ActuatorsRepository:
        return ActuatorsRepository(general.redis_config, actuators.conf)

    @singleton
    def sensors_repository(self) -> SensorsRepository:
        return SensorsRepository(general.redis_config, sensors.conf)

    @singleton
    def ifttt_rules_repository(self) -> IftttRulesRepository:
        return IftttRulesRepository(general.redis_config)

    @singleton
    def async_jobs(self) -> AsyncJobs:
        return AsyncJobs(general.redis_config)

    @singleton
    def email_notificator(self) -> EmailNotifier:
        return EmailNotifier(general.email['email'], general.email['password'], general.email['notifiedAddress'])

    @singleton
    def encriptors_builder(self) -> EncriptorsBuilder:
        return EncriptorsBuilder(general.communication['aes_key'])

    @singleton
    def actuator_strategies_builder(self) -> ActuatorStrategiesBuilder:
        return ActuatorStrategiesBuilder(self.communicator_registry(), self.actuators_repository(),
                                         actuators.conf, self.async_jobs())

    @singleton
    def actuator_commands(self) -> ActuatorCommands:
        return ActuatorCommands(self.actuator_strategies_builder(), self.encriptors_builder(),
                                self.actuators_repository())

    @singleton
    def text_sensor_data_parser(self) -> TextSensorDataParser:
        return TextSensorDataParser(self.sensors_repository())

    @singleton
    def home_defence(self) -> HomeDefence:
        return HomeDefence(self.actuator_commands(), self.sound_api(), self.actuators_repository())

    @singleton
    def authentication(self) -> Authentication:
        return Authentication(general.credentials)

    @singleton
    def actuator_token_converter(self) -> ActuatorTokenConverter:
        return ActuatorTokenConverter(self.actuators_repository())

    @singleton
    def sensors_token_converter(self) -> SensorTokenConverter:
        return SensorTokenConverter(self.sensors_repository())

    @singleton
    def tokenizer(self) -> Tokenizer:
        tokenizer = Tokenizer(self.root_logger())
        tokenizer.add_token_converter(self.actuator_token_converter())
        tokenizer.add_token_converter(self.sensors_token_converter())
        tokenizer.add_token_converter(CurrentTimeTokenConverter())
        tokenizer.add_token_converter(ActuatorStateTokenConverter())
        tokenizer.add_token_converter(BooleanTokenConverter())
        tokenizer.add_token_converter(IntTokenConverter())

        return tokenizer

    @singleton
    def change_actuator_listener(self) -> ChangeActuatorListener:
        return ChangeActuatorListener(self.actuator_commands())

    @singleton
    def fingerprint_door_unlock_listener(self) -> FingerprintDoorUnlockListener:
        return FingerprintDoorUnlockListener(self.actuator_commands(), self.authentication())

    @singleton
    def intruder_alert_listener(self) -> IntruderAlertListener:
        return IntruderAlertListener(self.actuators_repository(), self.email_notificator())

    @singleton
    def save_location_listener(self) -> SaveLocationListener:
        return SaveLocationListener(self.location_tracker_repository())

    @singleton
    def set_phone_is_home_listener(self) -> SetPhoneIsHomeListener:
        return SetPhoneIsHomeListener(general.home_coordonates, self.sensors_repository(),
                                      self.location_tracker_repository())

    @singleton
    def change_actuator_request_event(self) -> ChangeActuatorRequestEvent:
        return ChangeActuatorRequestEvent()

    @singleton
    def sensor_update_event(self) -> SensorUpdateEvent:
        return SensorUpdateEvent()

    @singleton
    def text_communication_enhancer(self) -> TextCommunicationEnhancer:
        return TextCommunicationEnhancer(self.tokenizer())

    @singleton
    def command_executor(self) -> CommandExecutor:
        return CommandExecutor(self.change_actuator_request_event(), self.text_communication_enhancer(),
                               self.sound_api(), self.root_logger())

    @singleton
    def expression_validator(self) -> ExpressionValidator:
        return ExpressionValidator(self.tokenizer())

    @singleton
    def voice_commands(self) -> VoiceCommands:
        return VoiceCommands(self.async_jobs(), self.root_logger()).configure()