import serial
import threading
import logging
import json
import time
from dateutil import tz
from datetime import datetime

import homeAutomationCommParser
from brain import brain
from dataContainer import dataContainer
from homeAutomationBt import btConnections
from jobControl import jobControll
from emailNotifier import emailNotifier
import config

btSeparator = '|'
btBuffer1 = btBuffer2 = "";

logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s] (%(threadName)-10s) %(message)s')
btComm = btConnections(
    config.btConns['bedroom'],
    config.btConns['living'],
    config.btConns['holway'])\
    .connectAllBt()
logging.debug('Finished connectiong to BT devices')

dataContainer = dataContainer(config.redisConfig)
jobControll = jobControll(config.redisConfig)
serialPort = serial.Serial("/dev/ttyAMA0", baudrate=9600, timeout=3.0)
emailNotif = emailNotifier(config.emailConfig['email'], config.emailConfig['password'], config.emailConfig['notifiedAddress'])
homeBrain = brain(btComm, serialPort, dataContainer, emailNotif)

# listens to a bluetooth connection until some data appears
# the format in which data arives is senzorName:senzorData with pipe separators between
def btSensorsPolling(btSeparator, btBuffer, dataContainer, btComm):
    while True:
        data = btComm.recv(10)
        btBuffer += data
        if btBuffer.endswith(btSeparator):
            btBuffer = btBuffer[:-1]
            logging.debug("senzors received : " + btBuffer)
            data = homeAutomationCommParser.parseSensorsString(btBuffer)
            for key, value in data.iteritems():
                homeBrain.sensorUpdate(key, value)
            logging.debug(dataContainer.getSensors())
            btBuffer = ''

# the jobManager thread listenes to a redis pub sub server for incoming jobs
def jobManager(dataContainer, jobControll, homeBrain):
    while True:
        for job in jobControll.listen():
            if job["data"] == 1:
                continue
            logging.debug(job["data"])
            jobData = json.loads(job["data"])
            if jobData["job_name"] == "actuators":
                homeBrain.changeActuator(jobData["actuator"], jobData["state"])

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



# initiating all threads
thr1 = threading.Thread(
    name='bedroomSenzorPooling',
    target=btSensorsPolling,
    args=(btSeparator, btBuffer1, dataContainer, btComm['bedroom'])
)
thr2 = threading.Thread(
    name='livingSenzorPooling',
    target=btSensorsPolling,
    args=(btSeparator, btBuffer2, dataContainer, btComm['living'])
)
thr3 = threading.Thread(
    name='jobManager',
    target=jobManager,
    args=(dataContainer, jobControll, homeBrain)
)
thr4 = threading.Thread(
    name='timeRulesControl',
    target=timeRulesControl,
    args=(dataContainer, homeBrain)
)

for thread in [thr1,  thr2, thr3, thr4]:
    thread.start()

