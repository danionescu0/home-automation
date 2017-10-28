from logging import RootLogger

from openzwave.network import ZWaveNetwork
from openzwave.option import ZWaveOption
from pydispatch import dispatcher

from communication.DeviceLifetimeCycles import DeviceLifetimeCycles


class ZWaveDevice(DeviceLifetimeCycles):
    def __init__(self, root_logger: RootLogger, port: str, openzwave_config_path: str) -> None:
        self.__root_logger = root_logger
        self.__port = port
        self.__openzwave_config_path = openzwave_config_path
        self.__network = None
        self.__state_change_callback = None

    def connect(self) -> None:
        options = ZWaveOption(self.__port, config_path=self.__openzwave_config_path, user_path=".", cmd_line="")
        options.set_console_output(False)
        options.set_save_log_level("None")
        options.set_logging(False)
        options.lock()
        self.__network = ZWaveNetwork(options, autostart=False)
        dispatcher.connect(self.__network_failed, ZWaveNetwork.SIGNAL_NETWORK_FAILED)
        dispatcher.connect(self.__network_ready, ZWaveNetwork.SIGNAL_NETWORK_READY)
        self.__network.start()

    def disconnect(self) -> None:
        self.__root_logger.debug('Disconnectiong Zwave device')
        self.__network.stop()

    def attach_state_change_callback(self, callback):
        self.__state_change_callback = callback

    def change_bistate_actuator(self, actuator_name: str, state: bool):
        if self.__network.state < self.__network.STATE_READY:
            return
        for node in self.__network.nodes:
            for val in self.__network.nodes[node].get_switches():
                self.__root_logger.debug(self.__network.nodes[node].values[val].id_on_network)
                if self.__network.nodes[node].values[val].id_on_network != actuator_name:
                    continue
                self.__root_logger.debug('Changing zwave switch: {0}'.format(actuator_name))
                self.__network.nodes[node].set_switch(val, state)

    def __network_failed(self, network):
        self.__root_logger.debug('Zwave network failed loading')

    def __network_ready(self, network):
        self.__root_logger.debug('Zwave network ready, contoller name: {0}'.format(network.controller))
        dispatcher.connect(self.__value_update, ZWaveNetwork.SIGNAL_VALUE)

    def __value_update(self, network, node, value):
        self.__root_logger.debug('Value {0} for node: {1}'.format(value, node))