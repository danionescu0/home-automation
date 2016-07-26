import json
import logging
import threading
import time

import configuration
from communication.ActuatorCommands import ActuatorCommands
from communication.CommunicatorFactory import CommunicatorFactory
from communication.SensorsMessageParser import SensorsMessageParser
from event.ChangeActuatorRequest import ChangeActuatorRequest
from event.SensorUpdate import SensorUpdate
from listener.ChangeActuatorListener import ChangeActuatorListener
from listener.SensorTriggeredRulesListener import SensorTriggeredRulesListener
from tools.DataContainer import DataContainer
from tools.TimeRules import TimeRules
from tools.EmailNotifier import EmailNotifier
from tools.JobControl import JobControll
from tools.HomeDefence import HomeDefence

logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s] (%(threadName)-10s) %(message)s')
bluetooth_communicator = CommunicatorFactory.create_communicator('bluetooth')
bluetooth_communicator.set_endpoint(configuration.bt_connections)
bluetooth_communicator.set_logger(logging)
bluetooth_communicator.connect()

data_container = DataContainer(configuration.redis_config)
time_rules = TimeRules(configuration.redis_config)
job_controll = JobControll(configuration.redis_config)
email_notif = EmailNotifier(configuration.email['email'], configuration.email['password'], configuration.email['notifiedAddress'])
actuator_commands = ActuatorCommands(bluetooth_communicator, data_container)
sensors_message_parser = SensorsMessageParser()
home_defence = HomeDefence(actuator_commands, configuration.burgler_sounds_folder, data_container)

change_actuator_listener = ChangeActuatorListener(actuator_commands)
sensor_triggered_rules_listener = SensorTriggeredRulesListener(data_container, email_notif, actuator_commands)
change_actuator_request = ChangeActuatorRequest()
sensor_update = SensorUpdate()

def communication(sensors_message_parser, data_container, sensor_update, bluetooth_communicator):
    def __sensor_callback(message):
        data = sensors_message_parser.parse_sensors_string(message)
        for sensorName, sensorValue in data.iteritems():
            data_container.set_sensor(sensorName, sensorValue)
            sensor_update.send(sensorName, sensorValue)
        logging.debug(data_container.get_sensors())

    bluetooth_communicator.listen(sensors_message_parser.is_buffer_parsable, __sensor_callback)

# the job_manager thread listenes to a redis pub sub server for incoming jobs
def job_manager(job_controll, change_actuator_request):
    def __job_callback(job_data):
        logging.debug(job_data)
        jobData = json.loads(job_data)
        if jobData["job_name"] == "actuators":
            change_actuator_request.send(jobData["actuator"], jobData["state"])

    job_controll.listen(__job_callback)

# periodically check if a time rules match the programmed interval and applies actuator changes
def time_rules_control(time_rules, change_actuator_request):
    while True:
        time.sleep(60)
        rules = time_rules.get_rules_that_match()
        for key, rule in rules.iteritems():
            logging.debug('Changing actuator {0} to state {1}'.format(rule['actuator'], rule['state']))
            change_actuator_request.send(rule['actuator'], rule['state'])

def defence(home_defence):
    while True:
        time.sleep(60)
        home_defence.iterate_burgler_mode()

threading.Thread(
    name='communication',
    target=communication,
    args=(sensors_message_parser, data_container, sensor_update, bluetooth_communicator)
).start()


threading.Thread(
    name='job_manager',
    target=job_manager,
    args=(job_controll, change_actuator_request)
).start()

threading.Thread(
    name='time_rules_control',
    target=time_rules_control,
    args=(time_rules, change_actuator_request)
).start()

threading.Thread(
    name='defence',
    target=defence,
    args=(home_defence,)
).start()