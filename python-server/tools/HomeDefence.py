import random
import datetime
import subprocess
from pytz import timezone
from astral import Astral

class HomeDefence:
    def __init__(self, actuatorCommands, burglerSoundsFolder, dataContainer):
        self.actuatorCommands = actuatorCommands
        self.burglerSoundsFolder = burglerSoundsFolder
        self.dataContainer = dataContainer
        self.lastBurglerLight = None
        self.burglerLights = ['livingLight', 'kitchenLight', 'hollwayLight']
        self.burglerMaxWaitBetweenActions = 3
        self.burglerSounds = 2

    def iterateBurglerMode(self):
        currentTime = datetime.datetime.now(timezone('Europe/Bucharest')).time()
        if self.__shouldRandomSkipIteration() or not self.__isAlarmSet():
            return

        self.__playRandomSound()
        if currentTime > datetime.time(22, 30, 00):
            return

        if self.__isOverSunset():
            return

        self.__toggleLights()


    def __shouldRandomSkipIteration(self):
        act = random.randint(0, self.burglerMaxWaitBetweenActions)
        return act != self.burglerMaxWaitBetweenActions

    def __isAlarmSet(self):
        actuators = self.dataContainer.getActuators()
        return actuators['homeAlarm']['state'] == True

    def __isOverSunset(self):
        astral = Astral()
        astral.solar_depression = 'civil'
        sun = astral['Bucharest'].sun(date=datetime.datetime.now(), local=True)
        currentTime = datetime.datetime.now(timezone('Europe/Bucharest')).time()
        return currentTime < sun['sunset'].time()

    def __toggleLights(self):
        if self.lastBurglerLight is not None:
            self.actuatorCommands.change_actuator(self.lastBurglerLight, False)
            self.lastBurglerLight = None
        else:
            self.lastBurglerLight = self.burglerLights[random.randint(0, 2)]
            self.actuatorCommands.change_actuator(self.lastBurglerLight, True)

    def __playRandomSound(self):
        process = subprocess.Popen(["mpg321", "-g", "150:D", self.__getBurglerSound()], stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        process.communicate()

    def __getBurglerSound(self):
        sound = random.randint(1, self.burglerSounds)
        path = "{}/p{}.mp3".format(self.burglerSoundsFolder, sound)
        return path