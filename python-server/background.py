import signal

from communication.IncommingTextStreamCommunicationThread import IncommingTextStreamCommunicationThread
from container import Container
from ifttt.IftttRulesThread import IftttRulesThread
from tools.AsyncJobsThread import AsyncJobsThread
from tools.HomeDefenceThread import HomeDefenceThread

container = Container()
root_logger = container.root_logger()
serial_communicator_registry = container.serial_communicator_registry()
async_actuator_commands = container.async_actuator_commands()
sensors_repo = container.sensors_repository()


change_actuator_listener = container.change_actuator_listener()
fingerprint_door_unlock_listener = container.fingerprint_door_unlock_listener()
intruder_alert_listener = container.intruder_alert_listener()
serial_communicator_registry.configure_communicators()
async_actuator_commands.connect()
wemo_switch = container.wemo_switch()
zwave_device = container.zwave_device()
device_lifetime_manager = container.device_lifetime_manager()
device_lifetime_manager\
    .add_device(wemo_switch)\
    .add_device(zwave_device)\
    .connect()

def main():
    threads = []
    threads.append(IncommingTextStreamCommunicationThread(container.text_sensor_data_parser(),
                                                          sensors_repo, container.sensor_update_event(),
                                                          serial_communicator_registry.get_communicator('bluetooth'), root_logger))
    threads.append(IncommingTextStreamCommunicationThread(container.text_sensor_data_parser(), sensors_repo,
                                                          container.sensor_update_event(),
                                                          serial_communicator_registry.get_communicator('serial'), root_logger))
    threads.append(container.incomming_zwave_communication_thread())
    threads.append(AsyncJobsThread(async_actuator_commands, container.change_actuator_request_event(), root_logger))
    threads.append(IftttRulesThread(container.ifttt_rules_repository(), container.command_executor(),
                                    container.tokenizer(), root_logger))
    threads.append(HomeDefenceThread(container.home_defence()))

    def handler(signum, frame):
        for thread in threads:
            thread.shutdown = True
        device_lifetime_manager.disconnect()

    signal.signal(signal.SIGINT, handler)
    signal.signal(signal.SIGTERM, handler)

    [thread.start() for thread in threads]
    for thread in threads:
        while thread.is_alive():
            thread.join(timeout=1)

if __name__ == '__main__':
    main()