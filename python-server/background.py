import sys

from communication.IncommingCommunicationThread import IncommingCommunicationThread
from communication.CommunicatorRegistry import CommunicatorRegistry
from communication.TextSensorDataParser import TextSensorDataParser
from communication.actuator.ActuatorCommands import ActuatorCommands
from config import actuators
from config import communication
from config import general
from config import sensors
from event.ChangeActuatorRequestEvent import ChangeActuatorRequestEvent
from event.SensorUpdateEvent import SensorUpdateEvent
from listener.ChangeActuatorListener import ChangeActuatorListener
from listener.FingerprintDoorUnlockListener import FingerprintDoorUnlockListener
from listener.IntruderAlertListener import IntruderAlertListener
from repository.Actuators import Actuators
from repository.IftttRules import IftttRules
from repository.Sensors import Sensors
from tools.Authentication import Authentication
from tools.EmailNotifier import EmailNotifier
from tools.HomeDefence import HomeDefence
from tools.HomeDefenceThread import HomeDefenceThread
from tools.IftttRulesThread import IftttRulesThread
from tools.JobControl import JobControll
from tools.JobControlThread import JobControlThread
from tools.TextToSpeech import TextToSpeech
from tools.LoggingConfig import LoggingConfig
from ifttt.command.CommandExecutor import CommandExecutor

logging_config = LoggingConfig(general.logging['log_file'], general.logging['log_entries'])
logging = logging_config.get_logger()
sys.excepthook = logging_config.set_error_hadler

comm_registry = CommunicatorRegistry(communication, logging)
comm_registry.configure_communicators()

text_to_speech = TextToSpeech()
actuators_repo = Actuators(general.redis_config, actuators.conf)
sensors_repo = Sensors(general.redis_config, sensors.conf)
ifttt_rules = IftttRules(general.redis_config)
job_controll = JobControll(general.redis_config)
email_notificator = EmailNotifier(general.email['email'], general.email['password'], general.email['notifiedAddress'])
actuator_commands = ActuatorCommands(comm_registry, actuators_repo, actuators.conf, job_controll)
text_sensor_data_parser = TextSensorDataParser(sensors.conf)
home_defence = HomeDefence(actuator_commands, general.burgler_sounds_folder, actuators_repo)
authentication = Authentication(general.credentials)

change_actuator_listener = ChangeActuatorListener(actuator_commands)
fingerprint_door_unlock_listener = FingerprintDoorUnlockListener(actuator_commands, authentication)
intruder_alert_listener = IntruderAlertListener(actuators_repo, email_notificator)
change_actuator_request_event = ChangeActuatorRequestEvent()
sensor_update_event = SensorUpdateEvent()
command_executor = CommandExecutor(change_actuator_request_event, text_to_speech, logging)

def main():
    threads = []
    threads.append(IncommingCommunicationThread(text_sensor_data_parser, sensors_repo, sensor_update_event,
                                                comm_registry.get_communicator('bluetooth')))
    threads.append(IncommingCommunicationThread(text_sensor_data_parser, sensors_repo, sensor_update_event,
                                                comm_registry.get_communicator('serial')))
    threads.append(JobControlThread(job_controll, change_actuator_request_event, logging))
    threads.append(IftttRulesThread(ifttt_rules, command_executor, sensors_repo, actuators_repo, logging))
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
