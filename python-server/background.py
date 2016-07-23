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
bluetooth_communicator.set_endpoint(config.bt_connections)
bluetooth_communicator.set_logger(logging)
bluetooth_communicator.connect()

data_container = DataContainer(config.redisConfig)
job_controll = JobControll(config.redisConfig)
email_notif = EmailNotifier(config.emailConfig['email'], config.emailConfig['password'], config.emailConfig['notifiedAddress'])
actuator_commands = ActuatorCommands(bluetooth_communicator, data_container)
sensors_message_parser = SensorsMessageParser()
home_defence = HomeDefence(actuator_commands, config.burgler_sounds_folder, data_container)

change_actuator_listener = ChangeActuatorListener(actuator_commands)
sensor_triggered_rules_listener = SensorTriggeredRulesListener(data_container, email_notif, actuator_commands)
change_actuator_request = ChangeActuatorRequest()
sensor_update = SensorUpdate()


# listens to a bluetooth connection until some data appears
# the format in which data arives is senzorName:senzorData with pipe separators between
def bt_senzors_polling(sensors_message_parser, data_container, sensor_update, bluetooth_communicator, bluetooth_address):
    def __sensor_callback(message):
        data = sensors_message_parser.parse_sensors_string(message)
        for sensorName, sensorValue in data.iteritems():
            data_container.set_sensor(sensorName, sensorValue)
            sensor_update.send(sensorName, sensorValue)
        logging.debug(data_container.get_sensors())

    bluetooth_communicator.set_receive_message_callback(__sensor_callback)
    bluetooth_communicator.listen_to_device(bluetooth_address, sensors_message_parser.is_buffer_parsable)


# the job_manager thread listenes to a redis pub sub server for incoming jobs
def job_manager(job_controll, change_actuator_request):
    def __job_callback(job_data):
        logging.debug(job_data)
        jobData = json.loads(job_data)
        if jobData["job_name"] == "actuators":
            change_actuator_request.send(jobData["actuator"], jobData["state"])

    job_controll.listen(__job_callback)


# periodically check if a time rules match the programmed interval
# if so the actuator is activated
def time_rules_control(data_container, change_actuator_request):
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

#connect to bluetooth devices
for bluetooth_device_name, bluetooth_address in config.bt_connections.iteritems():
    threading.Thread(
        name=bluetooth_device_name + '_thread',
        target=bt_senzors_polling,
        args=(sensors_message_parser, data_container, sensor_update, bluetooth_communicator, bluetooth_device_name)
    ).start()

threading.Thread(
    name='job_manager',
    target=job_manager,
    args=(job_controll, change_actuator_request)
).start()

threading.Thread(
    name='time_rules_control',
    target=time_rules_control,
    args=(data_container, change_actuator_request)
).start()

threading.Thread(
    name='defence',
    target=defence,
    args=(home_defence,)
).start()