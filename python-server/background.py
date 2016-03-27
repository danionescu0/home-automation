import serial
import threading
import logging
import json
import time
from dateutil import tz
from datetime import datetime

from brain import brain
from dataContainer import dataContainer
from btConnections import btConnections
from jobControl import jobControll
from communication import communication
from emailNotifier import emailNotifier
import config

btBuffer1 = btBuffer2 = btBuffer3 = btBuffer4 = ""

logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s] (%(threadName)-10s) %(message)s')
btComm = btConnections(
    config.btConns['bedroom'],
    config.btConns['living'],
    config.btConns['balcony'],
    config.btConns['holway'],
    config.btConns['fingerprint']
)
btComm.connectAllBt()
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
            logging.debug(rule['stringTime'])
            logging.debug(currentTime)
            if rule['stringTime'] != currentTime or rule['active'] != True:
                continue
            logging.debug("Changing actuator:", rule)
            homeBrain.changeActuator(rule["actuator"], rule["state"])

def burglerMode(homeBrain):
    while True:
        time.sleep(60)
        homeBrain.iterateBurglerMode()

# initiating all threads
thr1 = threading.Thread(
    name='bedroomSenzorPooling',
    target=btSensorsPolling,
    args=(communication, btBuffer1, dataContainer, btComm, 'bedroom')
)
thr2 = threading.Thread(
    name='livingSenzorPooling',
    target=btSensorsPolling,
    args=(communication, btBuffer2, dataContainer, btComm, 'living')
)
thr3 = threading.Thread(
    name='jobManager',
    target=jobManager,
    args=(jobControll, homeBrain)
)
thr4 = threading.Thread(
    name='timeRulesControl',
    target=timeRulesControl,
    args=(dataContainer, homeBrain)
)
thr5 = threading.Thread(
    name='burglerMode',
    target=burglerMode,
    args=(homeBrain,)
)
thr6 = threading.Thread(
    name='holwaySenzorPooling',
    target=btSensorsPolling,
    args=(communication, btBuffer3, dataContainer, btComm, 'holway')
)
thr7 = threading.Thread(
    name='fingerprintPooling',
    target=btSensorsPolling,
    args=(communication, btBuffer4, dataContainer, btComm, 'fingerprint')
)
for thread in [thr1,  thr2, thr3, thr4, thr5, thr6, thr7]:
    thread.start()

