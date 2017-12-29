import random
import datetime
from pytz import timezone
from logging import RootLogger

from typeguard import typechecked

from tools.DateUtils import DateUtils
from communication.actuator.ActuatorCommands import ActuatorCommands
from repository.ActuatorsRepository import ActuatorsRepository
from sound.SoundApi import SoundApi
from model.configuration.HomeDefenceCfg import HomeDefenceCfg


class HomeDefence:
    @typechecked()
    def __init__(self, actuator_commands: ActuatorCommands, sound_api: SoundApi,
                 actuators_repo: ActuatorsRepository, config: HomeDefenceCfg, logging: RootLogger):
        self.__actuator_commands = actuator_commands
        self.__sound_api = sound_api
        self.__actuators_repo = actuators_repo
        self.__last_burgler_light = None
        self.__config = config
        self.__logging = logging

    @typechecked()
    def iterate_burgler_mode(self) -> None:
        if not self.__config.enabled:
            return
        currentTime = datetime.datetime.now(timezone(DateUtils.get_timezone())).time()
        log_debug_message = 'Iterating burgler mode:'
        if self.__should_random_skip_iteration() or not self.__is_alarm_set():
            self.__logging.info(log_debug_message + ' Skipping iteration randomly')
            return

        log_debug_message += log_debug_message + ' Playing some sounds, '
        self.__play_random_sound()
        if currentTime > datetime.time(22, 30, 00):
            self.__logging.info(log_debug_message)
            return

        log_debug_message += log_debug_message + ' Toggling lights'
        if DateUtils.is_over_sunset():
            self.__logging.info(log_debug_message)
            self.__toggle_lights()

    def __should_random_skip_iteration(self):
        burgler_time_between_actions = self.__config.burgler_time_between_actions

        return random.randint(0, burgler_time_between_actions) != burgler_time_between_actions

    def __is_alarm_set(self):
        return self.__actuators_repo.get_actuator('homeAlarm').value is True

    def __toggle_lights(self):
        burgler_lights = self.__config.burgler_lights_switches
        if self.__last_burgler_light is not None:
            self.__actuator_commands.change_actuator(self.__last_burgler_light, False)
            self.__last_burgler_light = None
        else:
            self.__last_burgler_light = burgler_lights[random.randint(0, len(burgler_lights) - 1)]
            self.__actuator_commands.change_actuator(self.__last_burgler_light, True)

    def __play_random_sound(self):
        sounds = [
            'Whay are you dooing now'
            'What is the time'
            'Is anybody there'
        ]
        sound_nr = random.randint(0, len(sounds) - 1)
        self.__sound_api.say(sounds[sound_nr])