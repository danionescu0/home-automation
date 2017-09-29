import random
import datetime
from pytz import timezone

from typeguard import typechecked

from tools.DateUtils import DateUtils
from communication.actuator.ActuatorCommands import ActuatorCommands
from repository.ActuatorsRepository import ActuatorsRepository
from sound.SoundApi import SoundApi


class HomeDefence:
    # @ToDo move magic numbers to config
    @typechecked()
    def __init__(self, actuator_commands: ActuatorCommands, sound_api: SoundApi, actuators_repo: ActuatorsRepository):
        self.__actuator_commands = actuator_commands
        self.__sound_api = sound_api
        self.__actuators_repo = actuators_repo
        self.__last_burgler_light = None
        self.__burgler_lights = ['livingLight', 'kitchenLight', 'holwayLight']
        self._max_wait_between_actions = 3

    @typechecked()
    def iterate_burgler_mode(self) -> None:
        currentTime = datetime.datetime.now(timezone(DateUtils.get_timezone())).time()
        if self.__should_random_skip_iteration() or not self.__is_alarm_set():
            return

        self.__play_random_sound()
        if currentTime > datetime.time(22, 30, 00):
            return

        if not DateUtils.is_over_sunset():
            return

        self.__toggle_lights()

    def __should_random_skip_iteration(self):
        act = random.randint(0, self._max_wait_between_actions)

        return act != self._max_wait_between_actions

    def __is_alarm_set(self):
        actuators = self.__actuators_repo.get_actuators()

        return actuators['homeAlarm'].state == True

    def __toggle_lights(self):
        if self.__last_burgler_light is not None:
            self.__actuator_commands.change_actuator(self.__last_burgler_light, False)
            self.__last_burgler_light = None
        else:
            self.__last_burgler_light = self.__burgler_lights[random.randint(0, len(self.__burgler_lights) - 1)]
            self.__actuator_commands.change_actuator(self.__last_burgler_light, True)

    def __play_random_sound(self):
        sounds = [
            'Whay are you dooing now'
            'What is the time'
            'Is anybody there'
        ]
        sound_nr = random.randint(0, len(sounds) - 1)
        self.__sound_api.say[sounds[sound_nr]]