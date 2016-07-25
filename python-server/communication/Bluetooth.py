import bluetooth
from Base import Base

class Bluetooth(Base):
    RESOURCE_TEMPORARILY_UNAVAILABLE = '11'

    def send(self, which, value):
        try:
            self.__connections[which].send(value)
        except bluetooth.btcommon.BluetoothError as error:
            return self.__reconnect_bluetooth(which)

        return True

    def listen_to_device(self, bluetooth_address, complete_message_callback):
        message_buffer = ''
        while True:
            data = self.__receive(bluetooth_address, 10)
            if data == False:
                continue
                message_buffer += data
            if not complete_message_callback(message_buffer):
                continue
            self.get_receive_message_callback()(message_buffer)
            message_buffer = ''



    def listen(self, complete_message_callback, receive_message_callback):
        message_buffer = {}
        while True:
            for name, bluetooth_address in self.connection_mapping.iteritems():
                message_buffer[name] = ''
                data = self.__receive(name, 10)
                if data == False:
                    continue
                    message_buffer[name] += data
                if not complete_message_callback(message_buffer[name]):
                    continue
                receive_message_callback()(message_buffer[name])
                message_buffer[name] = ''

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
        self.connection_mapping = self.get_endpoint()
        self.__connections = {}
        for name, bluetooth_address in self.connection_mapping.iteritems():
            self.get_logger().debug("Connecting to {0} on address {1}".format(name, bluetooth_address))
            self.__connections[name] = self.__connnect_to_bluetooth(bluetooth_address, 1)
        self.get_logger().debug("Connected to all devices")

        return self

    def __reconnect_bluetooth(self, which):
        try:
            self.__connections[which] = self.__connnect_to_bluetooth(self.connection_mapping[which], 1)
        except bluetooth.btcommon.BluetoothError as error:
            return False

        return True

    def __connnect_to_bluetooth(self, id, ch):
        bt = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        bt.settimeout(None)
        bt.connect((id, ch))
        bt.setblocking(False)

        return bt