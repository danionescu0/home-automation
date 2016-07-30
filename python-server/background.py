import logging
import time

import configuration
from communication.ActuatorCommands import ActuatorCommands
from communication.CommunicatorFactory import CommunicatorFactory
from communication.SensorsMessageParser import SensorsMessageParser
from communication.CommunicationThread import CommunicationThread
from tools.JobControlThread import JobControlThread
from tools.TimeRulesControlThread import TimeRulesControlThread
from tools.HomeDefenceThread import HomeDefenceThread
from event.ChangeActuatorRequestEvent import ChangeActuatorRequestEvent
from event.SensorUpdateEvent import SensorUpdateEvent
from listener.ChangeActuatorListener import ChangeActuatorListener
from listener.CloseCourtainsOnRainListener import CloseCourtainsOnRainListener
from listener.FingerprintDoorUnlockListener import FingerprintDoorUnlockListener
from listener.IntruderAlertListener import IntruderAlertListener
from tools.DataContainer import DataContainer
from tools.TimeRules import TimeRules
from tools.EmailNotifier import EmailNotifier
from tools.JobControl import JobControll
from tools.HomeDefence import HomeDefence

# def main():
logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s] (%(threadName)-10s) %(message)s')
bluetooth_communicator = CommunicatorFactory.create_communicator('bluetooth')
bluetooth_communicator.set_endpoint(configuration.bt_connections)
bluetooth_communicator.set_logger(logging)
bluetooth_communicator.connect()

data_container = DataContainer(configuration.redis_config)
time_rules = TimeRules(configuration.redis_config)
job_controll = JobControll(configuration.redis_config)
email_notificator = EmailNotifier(configuration.email['email'], configuration.email['password'], configuration.email['notifiedAddress'])
actuator_commands = ActuatorCommands(bluetooth_communicator, data_container)
sensors_message_parser = SensorsMessageParser()
home_defence = HomeDefence(actuator_commands, configuration.burgler_sounds_folder, data_container)

change_actuator_listener = ChangeActuatorListener(actuator_commands)
fingerprint_door_unlock_listener = FingerprintDoorUnlockListener(data_container, actuator_commands)
close_courtains_on_rain_listener = CloseCourtainsOnRainListener(data_container, actuator_commands)
intruder_alert_listener = IntruderAlertListener(data_container, email_notificator)
change_actuator_request_event = ChangeActuatorRequestEvent()
sensor_update_event = SensorUpdateEvent()

threads = []
threads.append(CommunicationThread(sensors_message_parser, data_container, sensor_update_event, bluetooth_communicator))
threads.append(JobControlThread(job_controll, change_actuator_request_event, logging))
threads.append(TimeRulesControlThread(time_rules, change_actuator_request_event, logging))
threads.append(HomeDefenceThread(home_defence))

for thread in threads:
    thread.start()

# if __name__ == '__main__':
#     print 'here'
#     try:
#         main()
#     except KeyboardInterrupt:
#         print "shutdown"
#         shutdown = True
