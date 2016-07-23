import bluetooth
from Base import Base

class Bluetooth(Base):
    def send(self, which, value):
        try:
            self.bt_connections[which].send(value)
        except bluetooth.btcommon.BluetoothError as error:
            return self.__reconnect_bluetooth(which)

        return True

    def listen_to_device(self, bluetooth_address, untilCondition):
        message_buffer = ''
        while True:
            data = self.__receive(bluetooth_address, 10)
            if data == False:
                continue
                message_buffer += data
            if not untilCondition(message_buffer):
                continue
            self.get_receive_message_callback()(message_buffer)
            message_buffer = ''

    def __receive(self, which, size):
        try:
            received_data = self.bt_connections[which].recv(size)
            self.get_logger().debug("Senzors data received: " + received_data)
            return received_data

        except bluetooth.btcommon.BluetoothError as error:
            self.__reconnect_bluetooth(which)

        return False

    def connect(self):
        self.connection_mapping = self.get_endpoint()
        self.bt_connections = {}
        for name, connection_string in self.connection_mapping.iteritems():
            self.get_logger().debug("Connecting to {0} on address {1}".format(name, connection_string))
            self.bt_connections[name] = self.__connnect_to_bluetooth(connection_string, 1)
        self.get_logger().debug("Connected to all devices")

        return self

    def __reconnect_bluetooth(self, which):
        try:
            self.bt_connections[which] = self.__connnect_to_bluetooth(self.connection_mapping[which], 1)
        except bluetooth.btcommon.BluetoothError as error:
            return False

        return True

    def __connnect_to_bluetooth(self, id, ch):
        bt = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        bt.settimeout(None)
        bt.connect((id, ch))

        return bt