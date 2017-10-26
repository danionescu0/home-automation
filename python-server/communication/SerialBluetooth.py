from typing import Callable

import bluetooth
from typeguard import typechecked

from .BaseSerial import BaseSerial


class SerialBluetooth(BaseSerial):
    RESOURCE_TEMPORARILY_UNAVAILABLE = '11'

    @typechecked()
    def __init__(self, endpoint: dict):
        self.__endpoint = endpoint

    @typechecked()
    def send(self, which: str, value: bytes) -> bool:
        try:
            self.__connections[which].send(value)
        except bluetooth.btcommon.BluetoothError:
            return self.__reconnect_bluetooth(which)

        return True

    @typechecked()
    def listen(self, complete_message_callback: Callable[[str], bool], receive_message_callback: Callable[[str], None]):
        for name, bluetooth_address in self.connection_mapping.items():
            data = self.__receive(name, 10)
            if data == False:
                continue
            self.__message_buffer[name] += data
            if not complete_message_callback(self.__message_buffer[name]):
                continue
            receive_message_callback(self.__message_buffer[name])
            self.__message_buffer[name] = ''

    def __create_empty_message_buffer(self):
        message_buffer = {}
        for name, bluetooth_address in self.connection_mapping.items():
            message_buffer[name] = ''

        return message_buffer

    def __receive(self, which, size):
        try:
            received_data = self.__connections[which].recv(size).decode("utf-8")
            self.get_logger().debug("Senzors data received: " + received_data)
            return received_data

        except bluetooth.btcommon.BluetoothError:
            return False

        return False

    def connect(self) -> None:
        self.connection_mapping = self.__get_endpoint()
        self.__connections = {}
        for name, bluetooth_address in self.connection_mapping.items():
            self.get_logger().debug("Connecting to {0} on address {1}".format(name, bluetooth_address))
            self.__connections[name] = self.__connnect_to_bluetooth(bluetooth_address, 1)
        self.get_logger().debug("Connected to all devices")
        self.__message_buffer = self.__create_empty_message_buffer()

        return self

    def __reconnect_bluetooth(self, which):
        try:
            self.__connections[which] = self.__connnect_to_bluetooth(self.connection_mapping[which], 1)
        except bluetooth.btcommon.BluetoothError as error:
            return False

        return True

    def __connnect_to_bluetooth(self, id, ch):
        connection = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        connection.settimeout(None)
        print('connecting to:' + id)
        connection.connect((id, ch))
        connection.setblocking(False)

        return connection

    @typechecked()
    def disconnect(self) -> None:
        self.get_logger().debug("Disconnecting all bluetooth devices")
        [connection.close() for name, connection in self.__connections.items()]

    def __get_endpoint(self):
        return self.__endpoint