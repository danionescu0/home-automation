import logging

from communication.ActuatorCommands import ActuatorCommands
from communication.CommunicationThread import CommunicationThread
from communication.CommunicatorRegistry import CommunicatorRegistry
from communication.SensorsMessageParser import SensorsMessageParser
from config import actuators
from config import communication
from config import general
from config import sensors
from event.ChangeActuatorRequestEvent import ChangeActuatorRequestEvent
from event.SensorUpdateEvent import SensorUpdateEvent
from listener.ChangeActuatorListener import ChangeActuatorListener
from listener.CloseCourtainsOnRainListener import CloseCourtainsOnRainListener
from listener.FingerprintDoorUnlockListener import FingerprintDoorUnlockListener
from listener.IntruderAlertListener import IntruderAlertListener
from repository.TimeRules import TimeRules
from repository.Actuators import Actuators
from repository.Sensors import Sensors
from tools.Authentication import Authentication
from tools.EmailNotifier import EmailNotifier
from tools.HomeDefence import HomeDefence
from tools.HomeDefenceThread import HomeDefenceThread
from tools.JobControl import JobControll
from tools.JobControlThread import JobControlThread
from tools.TimeRulesControlThread import TimeRulesControlThread

logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s] (%(threadName)-10s) %(message)s')
comm_registry = CommunicatorRegistry(communication, logging)
comm_registry.configure_communicators()

actuators_repo = Actuators(general.redis_config, actuators.conf)
sensors_repo = Sensors(general.redis_config, sensors.conf)
time_rules = TimeRules(general.redis_config)
job_controll = JobControll(general.redis_config)
email_notificator = EmailNotifier(general.email['email'], general.email['password'], general.email['notifiedAddress'])
actuator_commands = ActuatorCommands(comm_registry, actuators_repo, actuators.conf)
sensors_message_parser = SensorsMessageParser()
home_defence = HomeDefence(actuator_commands, general.burgler_sounds_folder, actuators_repo)
authentication = Authentication(general.credentials)

change_actuator_listener = ChangeActuatorListener(actuator_commands)
fingerprint_door_unlock_listener = FingerprintDoorUnlockListener(actuator_commands, authentication)
close_courtains_on_rain_listener = CloseCourtainsOnRainListener(actuators_repo, actuator_commands)
intruder_alert_listener = IntruderAlertListener(actuators_repo, email_notificator)
change_actuator_request_event = ChangeActuatorRequestEvent()
sensor_update_event = SensorUpdateEvent()

def main():
    threads = []
    threads.append(CommunicationThread(sensors_message_parser, sensors_repo, sensor_update_event, comm_registry.get_communicator('bluetooth')))
    threads.append(JobControlThread(job_controll, change_actuator_request_event, logging))
    threads.append(TimeRulesControlThread(time_rules, change_actuator_request_event, logging))
    threads.append(HomeDefenceThread(home_defence))
    for thread in threads:
        thread.start()
    try:
        threads = [thread.join(1) for thread in threads if thread is not None and thread.isAlive()]
    except KeyboardInterrupt:
        print "Ctrl-c received! Sending kill to threads..."
        for thread in threads:
            thread.shutdown = True

if __name__ == '__main__':
    main()
