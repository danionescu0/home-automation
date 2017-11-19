from typing import Callable
from logging import RootLogger

from typeguard import typechecked
from openzwave.network import ZWaveNetwork
from openzwave.option import ZWaveOption
from pydispatch import dispatcher

from communication.DeviceLifetimeCycles import DeviceLifetimeCycles


class ZWaveDevice(DeviceLifetimeCycles):
    @typechecked()
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

    @typechecked()
    def attach_state_change_callback(self, callback: Callable[[str, float], None]):
        self.__state_change_callback = callback

    @typechecked()
    def change_switch(self, actuator_name: str, state: bool) -> bool:
        node, val = self.__get_node(actuator_name, 'switch')
        try:
            node.set_switch(val, state)
        except Exception as e:
            return False
        return True

    @typechecked()
    def change_dimmer(self, actuator_name: str, state: int) -> bool:
        node, val = self.__get_node(actuator_name, 'dimmer')
        try:
            node.set_dimmer(val, state)
        except Exception as e:
            return False
        return True

    @typechecked()
    def __get_node(self, actuator_name: str, type: str):
        if self.__network.state < self.__network.STATE_READY:
            return
        for node in self.__network.nodes:
            for val in self.__get_device_by_type(self.__network.nodes[node], type):
                self.__root_logger.debug('Zwave node: {0}'.format(
                    self.__network.nodes[node].values[val].id_on_network)
                )
                if self.__network.nodes[node].values[val].id_on_network != actuator_name:
                    continue
                self.__root_logger.debug('Changing zwave switch: {0}'.format(actuator_name))
                return self.__network.nodes[node], val

        raise Exception('Zwave node with id {0} not found'.format(actuator_name))

    @typechecked()
    def __get_device_by_type(self, node, type: str):
        if type == 'switch':
            return node.get_switches()
        elif type == 'dimmer':
            return node.get_dimmers()

    def __network_failed(self, network):
        self.__root_logger.debug('Zwave network failed loading')

    def __network_ready(self, network):
        self.__root_logger.debug('Zwave network ready, contoller name: {0}'.format(network.controller))
        dispatcher.connect(self.__value_update, ZWaveNetwork.SIGNAL_VALUE)

    def __value_update(self, network, node, value):
        self.__root_logger.debug('Id {0} for value: {1}'.format(value.id_on_network, value.data))
        self.__state_change_callback(value.id_on_network, value.data)