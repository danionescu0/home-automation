import random
import datetime
import subprocess
import time
from pytz import timezone
from astral import Astral

class brain:
    def __init__(self, btComm, burglerSoundsFolder, dataContainer, emailNotificator):
        self.btComm = btComm
        self.burglerSoundsFolder = burglerSoundsFolder
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
        lights = {'livingLight' : '1', 'bedroomLight' : '2', 'holwayLight' : '3', 'kitchenLight' : '4',
                  'closetLight' : '5', 'balconyLight' : '6'}
        if actuator == 'door':
            self.btComm.sendToBluetooth('holway', 'O')
        if actuator in lights:
            self.btComm.sendToBluetooth('living', lights[actuator])
            self.__writeActuatorState(state)
        if actuator == 'powerSocket1':
            self.btComm.sendToBluetooth('living', '8')
            self.__writeActuatorState(state)
        if actuator == 'livingCourtains':
            if state:
                self.btComm.sendToBluetooth('balcony', '1')
            else:
                self.btComm.sendToBluetooth('balcony', '0')
        if actuator == 'windowNodgeDown':
            self.btComm.sendToBluetooth('bedroom', '2')
        if actuator == 'window':
            if state:
                self.btComm.sendToBluetooth('bedroom', '1')
            else:
                self.btComm.sendToBluetooth('bedroom', '0')

    def __writeActuatorState(self, state):
        if (state):
            self.btComm.sendToBluetooth('living', 'O')
        else:
            self.btComm.sendToBluetooth('living', 'C')
        self.btComm.sendToBluetooth('living', '|')

    # Contains sensors triggers, when values changes
    # Todo split using event and listeners
    def sensorUpdate(self, name, value):
        self.dataContainer.setSensor(name, value)
        sensors = self.dataContainer.getSensors()
        actuators = self.dataContainer.getActuators()
        if name == 'rain' and sensors['rain'] > 40 and actuators['window']['state'] == False:
            self.btComm.sendToBluetooth('bedroom', '1')
            actuators['window']['state'] = True
            self.dataContainer.setActuator('window', True)
        if actuators['homeAlarm']['state'] == True and name == 'presence' and sensors['presence'] == 1:
            self.emailNotificator.sendAlert("Cineva a intrat in casa!", "Nasol naspa")
        if name == 'fingerprint' and sensors['fingerprint'] > -1:
            self.btComm.sendToBluetooth('holway', 'O')

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
            self.lastBurglerLight = None
        else:
            self.lastBurglerLight = self.burglerLights[random.randint(0, 2)]
            self.changeActuator(self.lastBurglerLight, True)

    def __getBurglerSound(self):
        sound = random.randint(1, self.burglerSounds)
        path = "{}/p{}.mp3".format(self.burglerSoundsFolder, sound)

        return path

