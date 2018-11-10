import signal

from communication.IncommingTextStreamCommunicationThread import IncommingTextStreamCommunicationThread
from container import Container
from ifttt.IftttRulesThread import IftttRulesThread
from tools.AsyncJobsThread import AsyncJobsThread
from tools.HomeDefenceThread import HomeDefenceThread

container = Container()
root_logger = container.root_logger()
async_actuator_commands = container.async_actuator_commands()
sensors_repo = container.sensors_repository()


listener_configurator = container.listener_configurator()
listener_configurator.initialise()
async_actuator_commands.connect()


device_lifetime_manager = container.device_lifetime_manager()
serial = container.serial()
bluetooth = container.bluetooth_serial()

device_lifetime_manager\
    .add_device('serial', serial)\
    .add_device('bluetooth', bluetooth) \
    .add_device('zwave', container.zwave_device()) \
    .connect()


def main():
    threads = []
    threads.append(IncommingTextStreamCommunicationThread(container.text_sensor_data_parser(), sensors_repo,
                                                          bluetooth, root_logger))
    threads.append(IncommingTextStreamCommunicationThread(container.text_sensor_data_parser(), sensors_repo,
                                                         serial, root_logger))
    threads.append(container.incomming_zwave_communication_thread())
    threads.append(AsyncJobsThread(async_actuator_commands, root_logger))
    threads.append(IftttRulesThread(container.ifttt_rules_repository(), container.command_executor(),
                                    container.tokenizer(), root_logger))
    threads.append(HomeDefenceThread(container.home_defence()))
    threads.append(container.sensors_polling_thread())

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