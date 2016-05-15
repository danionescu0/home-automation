import serial
import threading
import logging
import json
import time
import sys
from dateutil import tz
from datetime import datetime

from brain import brain
from dataContainer import dataContainer
from btConnections import btConnections
from jobControl import jobControll
from communication import communication
from emailNotifier import emailNotifier
import config

bluetoothBuffers = ['' for x in range(4)]

logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s] (%(threadName)-10s) %(message)s')
btComm = btConnections(config.btConnections).connect()
logging.debug('Finished connectiong to BT devices')

dataContainer = dataContainer(config.redisConfig)
jobControll = jobControll(config.redisConfig)
serialPort = serial.Serial("/dev/ttyAMA0", baudrate=9600, timeout=3.0)
emailNotif = emailNotifier(config.emailConfig['email'], config.emailConfig['password'], config.emailConfig['notifiedAddress'])
homeBrain = brain(btComm, config.burglerSoundsFolder, dataContainer, emailNotif)
communication = communication()

# listens to a bluetooth connection until some data appears
# the format in which data arives is senzorName:senzorData with pipe separators between
def btSensorsPolling(communication, btBuffer, dataContainer, btComm, btDeviceName):
    while True:
        data = btComm.reciveFromBluetooth(btDeviceName, 10)
        if data == False:
            continue
        btBuffer += data
        if communication.isBufferParsable(btBuffer):
            logging.debug("Senzors received: " + btBuffer)
            data = communication.parseSensorsString(btBuffer)
            for key, value in data.iteritems():
                homeBrain.sensorUpdate(key, value)
            logging.debug(dataContainer.getSensors())
            btBuffer = ''

# the jobManager thread listenes to a redis pub sub server for incoming jobs
def jobManager(jobControll, homeBrain):
    while True:
        for job in jobControll.listen():
            if job["data"] == 1:
                continue
            logging.debug(job["data"])
            jobData = json.loads(job["data"])
            if jobData["job_name"] == "actuators":
                homeBrain.changeActuator(jobData["actuator"], jobData["state"])

# periodically check if a time rules match the programmed interval
# if so the actuator is activated
def timeRulesControl(dataContainer, homeBrain):
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
            homeBrain.changeActuator(rule["actuator"], rule["state"])

def burglerMode(homeBrain):
    while True:
        time.sleep(60)
        homeBrain.iterateBurglerMode()

# initiating all threads
poolingThreads = [
    {'name' : 'bedroomSenzorPooling', 'deviceName' : 'bedroom', 'buffer': bluetoothBuffers[1]},
    {'name' : 'livingSenzorPooling', 'deviceName' : 'living', 'buffer': bluetoothBuffers[2]},
    {'name' : 'holwaySenzorPooling', 'deviceName' : 'holway', 'buffer': bluetoothBuffers[3]},
    # {'name' : 'bedroomSenzorPooling', 'deviceName' : 'bedroom'},
]

for threadData in poolingThreads:
    threading.Thread(
        name=threadData['name'],
        target=btSensorsPolling,
        args=(communication, threadData['buffer'], dataContainer, btComm, threadData['deviceName'])
    ).start()

threading.Thread(
    name='jobManager',
    target=jobManager,
    args=(jobControll, homeBrain)
).start()

threading.Thread(
    name='timeRulesControl',
    target=timeRulesControl,
    args=(dataContainer, homeBrain)
).start()

thr5 = threading.Thread(
    name='burglerMode',
    target=burglerMode,
    args=(homeBrain,)
).start()


