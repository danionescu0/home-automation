import bluetooth



class SerialBluetooth:
    RESOURCE_TEMPORARILY_UNAVAILABLE = '11'

    def __init__(self, connections: dict):
        self.__connections_mapping = connections

    def send(self, which: str, value: bytes) -> bool:
        try:
            self.__connections_mapping[which].send(value)
        except bluetooth.btcommon.BluetoothError:
            return self.__reconnect_bluetooth(which)

        return True

    def __create_empty_message_buffer(self):
        message_buffer = {}
        for name, bluetooth_address in self.connection_mapping.items():
            message_buffer[name] = ''

        return message_buffer

    def __receive(self, which, size):
        try:
            received_data = self.__connections_mapping[which].recv(size).decode("utf-8")
            print("Senzors data received: " + received_data)
            return received_data

        except bluetooth.btcommon.BluetoothError:
            return False

    def connect(self) -> None:
        self.connection_mapping = self.__connections_mapping
        self.__connections_mapping = {}
        for name, bluetooth_address in self.connection_mapping.items():
            self.__connections_mapping[name] = self.__connnect_to_bluetooth(bluetooth_address, 1)
        print("Connected to all bluetooth devices")
        self.__message_buffer = self.__create_empty_message_buffer()

        return self

    def __reconnect_bluetooth(self, which):
        try:
            self.__connections_mapping[which] = self.__connnect_to_bluetooth(self.connection_mapping[which], 1)
        except bluetooth.btcommon.BluetoothError as error:
            return False

        return True

    def __connnect_to_bluetooth(self, id, ch):
        connection = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        connection.settimeout(None)
        connection.connect((id, ch))
        connection.setblocking(False)

        return connection

    @typechecked()
    def disconnect(self) -> None:
        print("Disconnecting all bluetooth devices")
        [connection.close() for name, connection in self.__connections_mapping.items()]