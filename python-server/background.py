import json
import logging
import threading
import time
from datetime import datetime

from dateutil import tz

import config
from communication.ActuatorCommands import ActuatorCommands
from communication.CommunicatorFactory import CommunicatorFactory
from communication.SensorsMessageParser import SensorsMessageParser
from event.ChangeActuatorRequest import ChangeActuatorRequest
from event.SensorUpdate import SensorUpdate
from listener.ChangeActuatorListener import ChangeActuatorListener
from listener.SensorTriggeredRulesListener import SensorTriggeredRulesListener
from tools.DataContainer import DataContainer
from tools.EmailNotifier import EmailNotifier
from tools.JobControl import JobControll
from tools.HomeDefence import HomeDefence

logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s] (%(threadName)-10s) %(message)s')
bluetooth_communicator = CommunicatorFactory.create_communicator('bluetooth')
bluetooth_communicator.set_endpoint(config.btConnections)
bluetooth_communicator.connect()
logging.debug('Finished connectiong to BT devices')

data_container = DataContainer(config.redisConfig)
job_controll = JobControll(config.redisConfig)
email_notif = EmailNotifier(config.emailConfig['email'], config.emailConfig['password'], config.emailConfig['notifiedAddress'])
actuator_commands = ActuatorCommands(bluetooth_communicator, data_container)
sensors_message_parser = SensorsMessageParser()
home_defence = HomeDefence(actuator_commands, config.burglerSoundsFolder, data_container)

change_actuator_listener = ChangeActuatorListener(actuator_commands)
sensor_triggered_rules_listener = SensorTriggeredRulesListener(data_container, email_notif, actuator_commands)
change_actuator_request = ChangeActuatorRequest()
sensorUpdate = SensorUpdate()


# listens to a bluetooth connection until some data appears
# the format in which data arives is senzorName:senzorData with pipe separators between
def btSensorsPolling(sensors_message_parser, data_container, sensorUpdate, bluetooth_communicator, btDeviceName):
    def __sensorCallback(message):
        logging.debug("Senzors received: " + message)
        data = sensors_message_parser.parse_sensors_string(message)
        for sensorName, sensorValue in data.iteritems():
            data_container.set_sensor(sensorName, sensorValue)
            sensorUpdate.send(sensorName, sensorValue)
        logging.debug(data_container.get_sensors())

    bluetooth_communicator.set_receive_message_callback(__sensorCallback)
    bluetooth_communicator.listen_to_device(btDeviceName, sensors_message_parser.is_buffer_parsable)


# the jobManager thread listenes to a redis pub sub server for incoming jobs
def jobManager(job_controll, change_actuator_request):
    while True:
        for job in job_controll.listen():
            if job["data"] == 1:
                continue
            logging.debug(job["data"])
            jobData = json.loads(job["data"])
            if jobData["job_name"] == "actuators":
                change_actuator_request.send(jobData["actuator"], jobData["state"])

# periodically check if a time rules match the programmed interval
# if so the actuator is activated
def timeRulesControl(data_container, change_actuator_request):
    from_zone = tz.gettz('UTC')
    to_zone = tz.gettz('Europe/Bucharest')

    while True:
        time.sleep(60)
        rules = data_container.get_time_rules()
        initialDate = datetime.now().replace(tzinfo=from_zone)
        bucharestDate = initialDate.astimezone(to_zone)
        currentTime = bucharestDate.strftime('%H:%M:00')

        for key, rule in rules.iteritems():
            if rule['stringTime'] != currentTime or rule['active'] != True:
                continue
            logging.debug("Changing actuator:", rule)
            change_actuator_request.send(rule["actuator"], rule["state"])

def defence(home_defence):
    while True:
        time.sleep(60)
        home_defence.iterate_burgler_mode()

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
        args=(sensors_message_parser, data_container, sensorUpdate, bluetooth_communicator, threadData['deviceName'])
    ).start()

threading.Thread(
    name='jobManager',
    target=jobManager,
    args=(job_controll, change_actuator_request)
).start()

threading.Thread(
    name='timeRulesControl',
    target=timeRulesControl,
    args=(data_container, change_actuator_request)
).start()

threading.Thread(
    name='defence',
    target=defence,
    args=(home_defence,)
).start()