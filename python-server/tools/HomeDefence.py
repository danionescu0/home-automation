import random
import datetime
import subprocess
from pytz import timezone
from astral import Astral
from tools.DaytimeMoments import DaytimeMoments
class HomeDefence:
    def __init__(self, actuator_commands, burgler_sounds_folder, actuators_repo, ):
        self.actuator_commands = actuator_commands
        self.burgler_sounds_folder = burgler_sounds_folder
        self.actuators_repo = actuators_repo
        self.lastBurglerLight = None
        self.burglerLights = ['livingLight', 'kitchenLight', 'holwayLight']
        self.burglerMaxWaitBetweenActions = 3
        self.burglerSounds = 2

    def iterate_burgler_mode(self):
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
        act = random.randint(0, self.burglerMaxWaitBetweenActions)
        return act != self.burglerMaxWaitBetweenActions

    def __is_alarm_set(self):
        actuators = self.actuators_repo.get_actuators()
        return actuators['homeAlarm']['state'] == True

    def __toggle_lights(self):
        if self.lastBurglerLight is not None:
            self.actuator_commands.change_actuator(self.lastBurglerLight, False)
            self.lastBurglerLight = None
        else:
            self.lastBurglerLight = self.burglerLights[random.randint(0, 2)]
            self.actuator_commands.change_actuator(self.lastBurglerLight, True)

    def __play_random_sound(self):
        process = subprocess.Popen(["mpg321", "-g", "150:D", self.__get_burgler_sound()], stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        process.communicate()

    def __get_burgler_sound(self):
        sound = random.randint(1, self.burglerSounds)
        path = "{}/p{}.mp3".format(self.burgler_sounds_folder, sound)
        return path