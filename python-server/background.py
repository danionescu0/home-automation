import json
import logging
import threading
import time
from datetime import datetime
from dateutil import tz

import config
from tools.Brain import Brain
from tools.BtConnections import BtConnections
from tools.Communication import Communication
from tools.DataContainer import DataContainer
from tools.EmailNotifier import EmailNotifier
from tools.jobControl import JobControll
from event.ChangeActuatorRequest import ChangeActuatorRequest
from event.SensorUpdate import SensorUpdate
from listener.ChangeActuatorListener import ChangeActuatorListener
from listener.SensorTriggeredRulesListener import SensorTriggeredRulesListener

logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s] (%(threadName)-10s) %(message)s')
bluetoothBuffers = ['' for x in range(5)]
btComm = BtConnections(config.btConnections).connect()
logging.debug('Finished connectiong to BT devices')

dataContainer = DataContainer(config.redisConfig)
jobControll = JobControll(config.redisConfig)
emailNotif = EmailNotifier(config.emailConfig['email'], config.emailConfig['password'], config.emailConfig['notifiedAddress'])
homeBrain = Brain(btComm, config.burglerSoundsFolder, dataContainer)
communication = Communication()

changeActuatorListener = ChangeActuatorListener(homeBrain)
sensorTriggeredRulesListener = SensorTriggeredRulesListener(dataContainer, emailNotif, homeBrain)
changeActuatorRequest = ChangeActuatorRequest()
sensorUpdate = SensorUpdate()


# listens to a bluetooth connection until some data appears
# the format in which data arives is senzorName:senzorData with pipe separators between
def btSensorsPolling(communication, btBuffer, dataContainer, sensorUpdate, btComm, btDeviceName):
    while True:
        data = btComm.reciveFromBluetooth(btDeviceName, 10)
        if data == False:
            continue
        btBuffer += data
        if communication.isBufferParsable(btBuffer):
            logging.debug("Senzors received: " + btBuffer)
            data = communication.parseSensorsString(btBuffer)
            for sensorName, sensorValue in data.iteritems():
                dataContainer.setSensor(sensorName, sensorValue)
                sensorUpdate.send(sensorName, sensorValue)

            logging.debug(dataContainer.getSensors())
            btBuffer = ''

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

# initiating all threads
poolingThreads = [
    {'name' : 'bedroomSenzorPooling', 'deviceName' : 'bedroom', 'buffer': bluetoothBuffers[1]},
    {'name' : 'livingSenzorPooling', 'deviceName' : 'living', 'buffer': bluetoothBuffers[2]},
    {'name' : 'holwaySenzorPooling', 'deviceName' : 'holway', 'buffer': bluetoothBuffers[3]},
    # {'name' : 'fingerprintSenzorPooling', 'deviceName' : 'fingerprint', 'buffer': bluetoothBuffers[4]},
]

for threadData in poolingThreads:
    threading.Thread(
        name=threadData['name'],
        target=btSensorsPolling,
        args=(communication, threadData['buffer'], dataContainer, sensorUpdate, btComm, threadData['deviceName'])
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

thr5 = threading.Thread(
    name='burglerMode',
    target=burglerMode,
    args=(homeBrain,)
).start()