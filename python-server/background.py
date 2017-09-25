import signal
import sys

from config import actuators
from config import general
from config import sensors

from communication.CommunicatorRegistry import CommunicatorRegistry
from communication.IncommingCommunicationThread import IncommingCommunicationThread
from communication.TextSensorDataParser import TextSensorDataParser
from communication.actuator.ActuatorCommands import ActuatorCommands
from communication.actuator.ActuatorStrategiesBuilder import ActuatorStrategiesBuilder
from communication.encriptors.EncriptorsBuilder import EncriptorsBuilder

from event.ChangeActuatorRequestEvent import ChangeActuatorRequestEvent
from event.SensorUpdateEvent import SensorUpdateEvent
from ifttt.command.CommandExecutor import CommandExecutor
from ifttt.parser.Tokenizer import Tokenizer
from ifttt.command.TextCommunicationEnhancer import TextCommunicationEnhancer
from listener.ChangeActuatorListener import ChangeActuatorListener
from listener.FingerprintDoorUnlockListener import FingerprintDoorUnlockListener
from listener.IntruderAlertListener import IntruderAlertListener
from repository.Actuators import Actuators
from repository.IftttRules import IftttRules
from repository.Sensors import Sensors
from sound.RemoteSpeaker import RemoteSpeaker
from tools.Authentication import Authentication
from tools.EmailNotifier import EmailNotifier
from tools.HomeDefence import HomeDefence
from tools.HomeDefenceThread import HomeDefenceThread
from tools.IftttRulesThread import IftttRulesThread
from tools.AsyncJobs import AsyncJobs
from tools.AsyncJobsThread import AsyncJobsThread
from tools.LoggingConfig import LoggingConfig

logging_config = LoggingConfig(general.logging['log_file'], general.logging['log_entries'])
logging = logging_config.get_logger()
sys.excepthook = logging_config.set_error_hadler

comm_registry = CommunicatorRegistry(general.communication, logging)
comm_registry.configure_communicators()

sound_api = RemoteSpeaker(general.remote_speaker['host'], general.remote_speaker['user'], general.remote_speaker['password'])
actuators_repo = Actuators(general.redis_config, actuators.conf)
sensors_repo = Sensors(general.redis_config, sensors.conf)
ifttt_rules = IftttRules(general.redis_config)
async_jobs = AsyncJobs(general.redis_config)
async_jobs.connect()
email_notificator = EmailNotifier(general.email['email'], general.email['password'], general.email['notifiedAddress'])
encriptiors_builder = EncriptorsBuilder(general.communication['aes_key'])
actuator_strategies_builder = ActuatorStrategiesBuilder(comm_registry, actuators_repo, actuators.conf, async_jobs)
actuator_commands = ActuatorCommands(actuator_strategies_builder, encriptiors_builder, actuators_repo, actuators.conf)
text_sensor_data_parser = TextSensorDataParser(sensors.conf)
home_defence = HomeDefence(actuator_commands, sound_api, actuators_repo)
authentication = Authentication(general.credentials)
tokenizer = Tokenizer(sensors_repo, actuators_repo)

e1 = ChangeActuatorListener(actuator_commands)
e2 = FingerprintDoorUnlockListener(actuator_commands, authentication)
e3 = IntruderAlertListener(actuators_repo, email_notificator)

change_actuator_request_event = ChangeActuatorRequestEvent()
sensor_update_event = SensorUpdateEvent()
text_communication_enhancer = TextCommunicationEnhancer(tokenizer)
command_executor = CommandExecutor(change_actuator_request_event, text_communication_enhancer, sound_api, logging)

def main():
    threads = []
    threads.append(IncommingCommunicationThread(text_sensor_data_parser, sensors_repo, sensor_update_event,
                                                comm_registry.get_communicator('bluetooth'), logging))
    threads.append(IncommingCommunicationThread(text_sensor_data_parser, sensors_repo, sensor_update_event,
                                                comm_registry.get_communicator('serial'), logging))
    threads.append(AsyncJobsThread(async_jobs, change_actuator_request_event, logging))
    threads.append(IftttRulesThread(ifttt_rules, command_executor, tokenizer, logging))
    threads.append(HomeDefenceThread(home_defence))
    def handler(signum, frame):
        for thread in threads:
            thread.shutdown = True

    signal.signal(signal.SIGINT, handler)
    signal.signal(signal.SIGTERM, handler)

    [thread.start() for thread in threads]
    for thread in threads:
        while thread.is_alive():
            thread.join(timeout=1)

if __name__ == '__main__':
    main()
