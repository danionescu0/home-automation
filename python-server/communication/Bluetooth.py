import bluetooth
from Base import Base

class Bluetooth(Base):
    def send(self, which, value):
        try:
            self.btConnections[which].send(value)
        except bluetooth.btcommon.BluetoothError as error:
            return self.__reconnect_bluetooth(which)

        return True

    def listen_to_device(self, deviceName, untilCondition):
        messageBuffer = ''
        while True:
            data = self.__receive(deviceName, 10)
            if data == False:
                continue
            messageBuffer += data
            if not untilCondition(messageBuffer):
                continue
            self.get_receive_message_callback()(messageBuffer)
            messageBuffer = ''

    def __receive(self, which, howMuch):
        try:
            return self.btConnections[which].recv(howMuch)
        except bluetooth.btcommon.BluetoothError as error:
            self.__reconnect_bluetooth(which)

        return False

    def connect(self):
        self.connectionMapping = self.get_endpoint()
        self.btConnections = {}
        for name, connectionString in self.connectionMapping.iteritems():
            self.btConnections[name] = self.__connnect_to_bluetooth(connectionString, 1)

        return self

    def __reconnect_bluetooth(self, which):
        try:
            self.btConnections[which] = self.__connnect_to_bluetooth(self.connectionMapping[which], 1)
        except bluetooth.btcommon.BluetoothError as error:
            return False

        return True

    def __connnect_to_bluetooth(self, id, ch):
        bt = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        bt.settimeout(None)
        bt.connect((id, ch))

        return bt