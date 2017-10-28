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

    def connect(self) -> None:
        options = ZWaveOption(self.__port, config_path=self.__openzwave_config_path, user_path=".", cmd_line="")
        options.set_console_output(True)
        options.set_save_log_level("None")
        options.set_logging(True)
        options.lock()

        def louie_network_failed(network):
            self.__root_logger.debug('Zwave network failed loading')

        def louie_network_ready(network):
            print("Hello from network : I'm ready : {} nodes were found.".format(network.nodes_count))
            print("Hello from network : my controller is : {}".format(network.controller))
            dispatcher.connect(louie_node_update, ZWaveNetwork.SIGNAL_NODE)
            dispatcher.connect(louie_value_update, ZWaveNetwork.SIGNAL_VALUE)

        def louie_node_update(network, node):
            print("Hello from node : {}.".format(node))

        def louie_value_update(network, node, value):
            print("Hello from value : {}.".format(value))

        self.__network = ZWaveNetwork(options, autostart=False)
        dispatcher.connect(louie_network_failed, ZWaveNetwork.SIGNAL_NETWORK_FAILED)
        dispatcher.connect(louie_network_ready, ZWaveNetwork.SIGNAL_NETWORK_READY)
        self.__network.start()

    def disconnect(self) -> None:
        self.__root_logger.debug('Disconnectiong Zwave device')
        self.__network.stop()

    def change_bistate_actuator(self, actuator_name: str, state: bool):
        if self.__network.state < self.__network.STATE_READY:
            return
        for node in self.__network.nodes:
            for val in self.__network.nodes[node].get_switches():
                self.__root_logger.debug(self.__network.nodes[node].values[val].id_on_network)
                if self.__network.nodes[node].values[val].id_on_network != actuator_name:
                    continue
                self.__network.nodes[node].set_switch(val, state)