import bluetooth
from Base import Base

class Bluetooth(Base):
    RESOURCE_TEMPORARILY_UNAVAILABLE = '11'

    def __init__(self, endpoint):
        self.__endpoint = endpoint

    def send(self, which, value):
        try:
            self.__connections[which].send(value)
        except bluetooth.btcommon.BluetoothError as error:
            return self.__reconnect_bluetooth(which)

        return True

    def listen(self, complete_message_callback, receive_message_callback):
        for name, bluetooth_address in self.connection_mapping.iteritems():
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
        for name, bluetooth_address in self.connection_mapping.iteritems():
            message_buffer[name] = ''

        return message_buffer

    def __receive(self, which, size):
        try:
            received_data = self.__connections[which].recv(size)
            self.get_logger().debug("Senzors data received: " + received_data)
            return received_data

        except bluetooth.btcommon.BluetoothError as error:
            if self.RESOURCE_TEMPORARILY_UNAVAILABLE in error.message:
                return False
            self.__reconnect_bluetooth(which)

        return False

    def connect(self):
        self.connection_mapping = self.__get_endpoint()
        self.__connections = {}
        for name, bluetooth_address in self.connection_mapping.iteritems():
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
        connection.connect((id, ch))
        connection.setblocking(False)

        return connection

    def disconnect(self):
        self.get_logger().debug("Disconnecting all bluetooth devices")
        for name, connection in self.__connections.iteritems():
            connection.close()

    def __get_endpoint(self):
        return self.__endpoint