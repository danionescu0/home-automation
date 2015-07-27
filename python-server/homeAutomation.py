import serial
import threading
import logging
import json

import homeAutomationCommParser
from brain import brain
from dataContainer import dataContainer
from homeAutomationBt import btConnections
from jobControl import jobControll
import config

btSeparator = '|'
btBuffer1 = btBuffer2 = "";

logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s] (%(threadName)-10s) %(message)s')
btComm = btConnections(config.btConns['bedroom'], config.btConns['living']).connectAllBt()
logging.debug('Finished connectiong to BT devices')
dataContainer = dataContainer(config.redisConfig)
jobControll = jobControll(config.redisConfig)
serialPort = serial.Serial("/dev/ttyAMA0", baudrate=9600, timeout=3.0)
homeBrain = brain(btComm, serialPort, dataContainer)

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
                dataContainer.setSensor(key, value)
                homeBrain.sensorsUpdate(key)
            logging.debug(dataContainer.getSensors())
            btBuffer = ''

# the jobManager thread listenes to a redis pub sub server for incoming jobs
def jobManager(dataContainer, jobControll, homeBrain):
    while True:
        for job in jobControll.listen():
            if job["data"] == 1:
                continue
            print job["data"]
            jobData = json.loads(job["data"])
            if jobData["job_name"] == "actuators":
                homeBrain.changeActuator(jobData["actuator"], jobData["state"])

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
for thread in [thr1, thr2, thr3]:
    thread.start()

