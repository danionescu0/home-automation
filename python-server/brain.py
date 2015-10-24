import random
import datetime
import subprocess
import time
from pytz import timezone
from astral import Astral

class brain:
    def __init__(self, btComm, serial, dataContainer, emailNotificator):
        self.btComm = btComm
        self.serial = serial
        self.dataContainer = dataContainer
        self.emailNotificator = emailNotificator
        self.lastBurglerLight = None
        self.burglerLights = ['livingLight', 'kitchenLight', 'bedroomLight']
        self.burglerMaxWaitBetweenActions = 3
        self.burglerSounds = 2

    def changeActuator(self, actuator, state):
        self.dataContainer.setActuator(actuator, state)
        if actuator != 'closeAllLights':
            self.__doChangeActuator(actuator, state)
            return

        allActuators = self.dataContainer.getActuators()

        for name, propreties in allActuators.iteritems():
            if propreties['device'] == 'light':
                self.dataContainer.setActuator(name, False)
                self.__doChangeActuator(name, False)
                time.sleep(3)

    def __doChangeActuator(self, actuator, state):
        if actuator == 'door':
            self.btComm['holway'].send("O")
        if actuator == 'livingLight':
            self.serial.write("1")
            self.__writeActuatorState(state)
        if actuator == 'bedroomLight':
            self.serial.write("2")
            self.__writeActuatorState(state)
        if actuator == 'holwayLight':
            self.serial.write("3")
            self.__writeActuatorState(state)
        if actuator == 'kitchenLight':
            self.serial.write("4")
            self.__writeActuatorState(state)
        if actuator == 'powerSocket1':
            self.serial.write("8")
            self.__writeActuatorState(state)
        if actuator == 'window':
            if state:
               self.btComm['bedroom'].send("1")
            else:
               self.btComm['bedroom'].send("0")

    def __writeActuatorState(self, state):
        if (state):
            self.serial.write("O")
        else:
            self.serial.write("C")
        self.serial.write("|");

    def sensorUpdate(self, name, value):
        self.dataContainer.setSensor(name, value)
        sensors = self.dataContainer.getSensors()
        actuators = self.dataContainer.getActuators()
        if name == 'rain' and sensors['rain'] > 40 and actuators['window']['state'] == False:
            self.btComm['bedroom'].send("1")
            actuators['window']['state'] = True
            self.dataContainer.setActuator('window', True)
        if actuators['homeAlarm']['state'] == True and name == 'presence' and sensors['presence'] == 1:
            self.emailNotificator.sendAlert("Cineva a intrat in casa!", "Nasol naspa")

    def iterateBurglerMode(self):
        actuators = self.dataContainer.getActuators()
        currentTime = datetime.datetime.now(timezone('Europe/Bucharest')).time()
        if actuators['homeAlarm']['state'] == False:
            return

        act = random.randint(0, self.burglerMaxWaitBetweenActions)
        print(act)
        if act != self.burglerMaxWaitBetweenActions:
            return
        astral = Astral()
        astral.solar_depression = 'civil'
        sun = astral['Bucharest'].sun(date=datetime.datetime.now(), local=True)

        if currentTime < sun['sunset'].time() or currentTime > datetime.time(22, 30, 00):
            return
        p = subprocess.Popen(["mpg321", "-a", "bluetooth", "-g", "150:D"
                                                                 "", self.__getBurglerSound()],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        p.communicate()
        if self.lastBurglerLight is not None:
            self.changeActuator(self.lastBurglerLight, False)
            print("Changing to false")
            print(self.lastBurglerLight)
            self.lastBurglerLight = None
        else:
            self.lastBurglerLight = self.burglerLights[random.randint(0, 2)]
            self.changeActuator(self.lastBurglerLight, True)
            print("Changing to true")
            print(self.lastBurglerLight)

    def __getBurglerSound(self):
        sound = random.randint(1, self.burglerSounds)
        path = "/home/pi/Downloads/p{}.mp3".format(sound)

        return path

