import json
import logging
import threading
import time
import config
from datetime import datetime
from dateutil import tz
from communication.CommunicatorFactory import CommunicatorFactory

from communication.Bluetooth import Bluetooth
from event.ChangeActuatorRequest import ChangeActuatorRequest
from event.SensorUpdate import SensorUpdate
from listener.ChangeActuatorListener import ChangeActuatorListener
from listener.SensorTriggeredRulesListener import SensorTriggeredRulesListener
from tools.Brain import Brain
from tools.DataContainer import DataContainer
from tools.EmailNotifier import EmailNotifier
from tools.SensorsMessageParser import SensorsMessageParser
from tools.jobControl import JobControll

logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s] (%(threadName)-10s) %(message)s')
bluetoothCommunicator = CommunicatorFactory.createCommunicator('bluetooth')
bluetoothCommunicator.setEndpoint(config.btConnections)
bluetoothCommunicator.connect()
logging.debug('Finished connectiong to BT devices')

dataContainer = DataContainer(config.redisConfig)
jobControll = JobControll(config.redisConfig)
emailNotif = EmailNotifier(config.emailConfig['email'], config.emailConfig['password'], config.emailConfig['notifiedAddress'])
homeBrain = Brain(bluetoothCommunicator, config.burglerSoundsFolder, dataContainer)
sensorsMessageParser = SensorsMessageParser()

changeActuatorListener = ChangeActuatorListener(homeBrain)
sensorTriggeredRulesListener = SensorTriggeredRulesListener(dataContainer, emailNotif, homeBrain)
changeActuatorRequest = ChangeActuatorRequest()
sensorUpdate = SensorUpdate()


# listens to a bluetooth connection until some data appears
# the format in which data arives is senzorName:senzorData with pipe separators between
def btSensorsPolling(sensorsMessageParser, dataContainer, sensorUpdate, bluetoothCommunicator, btDeviceName):
    def __sensorCallback(message):
        logging.debug("Senzors received: " + message)
        data = sensorsMessageParser.parseSensorsString(message)
        for sensorName, sensorValue in data.iteritems():
            dataContainer.setSensor(sensorName, sensorValue)
            sensorUpdate.send(sensorName, sensorValue)
        logging.debug(dataContainer.getSensors())

    bluetoothCommunicator.setReceiveMessageCallback(__sensorCallback)
    bluetoothCommunicator.listenToDevice(btDeviceName, sensorsMessageParser.isBufferParsable)


# the jobManager thread listenes to a redis pub sub server for incoming jobs
def jobManager(jobControll, changeActuatorRequest):
    while True:
        for job in jobControll.listen():
            if job["data"] == 1:
                continue
            logging.debug(job["data"])
            jobData = json.loads(job["data"])
            if jobData["job_name"] == "actuators":
                changeActuatorRequest.send(jobData["actuator"], jobData["state"])

# periodically check if a time rules match the programmed interval
# if so the actuator is activated
def timeRulesControl(dataContainer, changeActuatorRequest):
    from_zone = tz.gettz('UTC')
    to_zone = tz.gettz('Europe/Bucharest')

    while True:
        time.sleep(60)
        rules = dataContainer.getTimeRules()
        initialDate = datetime.now().replace(tzinfo=from_zone)
        bucharestDate = initialDate.astimezone(to_zone)
        currentTime = bucharestDate.strftime('%H:%M:00')

        for key, rule in rules.iteritems():
            if rule['stringTime'] != currentTime or rule['active'] != True:
                continue
            logging.debug("Changing actuator:", rule)
            changeActuatorRequest.send(rule["actuator"], rule["state"])

def burglerMode(homeBrain):
    while True:
        time.sleep(60)
        homeBrain.iterateBurglerMode()

poolingThreads = [
    {'name' : 'bedroomSenzorPooling', 'deviceName' : 'bedroom'},
    {'name' : 'livingSenzorPooling', 'deviceName' : 'living'},
    {'name' : 'holwaySenzorPooling', 'deviceName' : 'holway'},
    # {'name' : 'fingerprintSenzorPooling', 'deviceName' : 'fingerprint'},
]

for threadData in poolingThreads:
    threading.Thread(
        name=threadData['name'],
        target=btSensorsPolling,
        args=(sensorsMessageParser, dataContainer, sensorUpdate, bluetoothCommunicator, threadData['deviceName'])
    ).start()

threading.Thread(
    name='jobManager',
    target=jobManager,
    args=(jobControll, changeActuatorRequest)
).start()

threading.Thread(
    name='timeRulesControl',
    target=timeRulesControl,
    args=(dataContainer, changeActuatorRequest)
).start()

threading.Thread(
    name='burglerMode',
    target=burglerMode,
    args=(homeBrain,)
).start()