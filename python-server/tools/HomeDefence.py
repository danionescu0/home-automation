import random
import datetime
from pytz import timezone
from typeguard import typechecked

from tools.DaytimeMoments import DaytimeMoments
from communication.actuator.ActuatorCommands import ActuatorCommands
from repository.Actuators import Actuators

class HomeDefence:
    # @ToDo move magic numbers to config
    @typechecked()
    def __init__(self, actuator_commands: ActuatorCommands, burgler_sounds_folder: str, actuators_repo: Actuators):
        self.actuator_commands = actuator_commands
        self.burgler_sounds_folder = burgler_sounds_folder
        self.actuators_repo = actuators_repo
        self.last_burgler_light = None
        self.burgler_lights = ['livingLight', 'kitchenLight', 'holwayLight']
        self.max_wait_between_actions = 3
        self.burgler_sounds = 2

    @typechecked()
    def iterate_burgler_mode(self) -> None:
        currentTime = datetime.datetime.now(timezone('Europe/Bucharest')).time()
        if self.__should_random_skip_iteration() or not self.__is_alarm_set():
            return

        self.__play_random_sound()
        if currentTime > datetime.time(22, 30, 00):
            return

        if not DaytimeMoments.is_over_sunset():
            return

        self.__toggle_lights()

    def __should_random_skip_iteration(self):
        act = random.randint(0, self.max_wait_between_actions)

        return act != self.max_wait_between_actions

    def __is_alarm_set(self):
        actuators = self.actuators_repo.get_actuators()

        return actuators['homeAlarm']['state'] == True

    def __toggle_lights(self):
        if self.last_burgler_light is not None:
            self.actuator_commands.change_actuator(self.last_burgler_light, False)
            self.last_burgler_light = None
        else:
            self.last_burgler_light = self.burgler_lights[random.randint(0, 2)]
            self.actuator_commands.change_actuator(self.last_burgler_light, True)

    # @ToDo implement an api call to a device that plays sounds
    def __play_random_sound(self):
        pass

    def __get_burgler_sound(self):
        sound = random.randint(1, self.burgler_sounds)
        path = "{}/p{}.mp3".format(self.burgler_sounds_folder, sound)

        return path