import bluetooth
from Base import Base

class Bluetooth(Base):
    def send(self, which, value):
        try:
            self.btConnections[which].send(value)
        except bluetooth.btcommon.BluetoothError as error:
            return self.__reconnectBluetooth(which)

        return True

    def listenToDevice(self, deviceName, untilCondition):
        messageBuffer = ''
        while True:
            data = self.__receive(deviceName, 10)
            if data == False:
                continue
            messageBuffer += data
            if not untilCondition(messageBuffer):
                continue
            self.getReceiveMessageCallback()(messageBuffer)

    def __receive(self, which, howMuch):
        try:
            return self.btConnections[which].recv(howMuch)
        except bluetooth.btcommon.BluetoothError as error:
            self.__reconnectBluetooth(which)

        return False

    def connect(self):
        self.connectionMapping = self.getEndpoint()
        self.btConnections = {}
        for name, connectionString in self.connectionMapping.iteritems():
            self.btConnections[name] = self.__connnectToBluetooth(connectionString, 1)

        return self

    def __reconnectBluetooth(self, which):
        try:
            self.btConnections[which] = self.__connnectToBluetooth(self.connectionMapping[which], 1)
        except bluetooth.btcommon.BluetoothError as error:
            return False

        return True

    def __connnectToBluetooth(self, id, ch):
        bt = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        bt.settimeout(None)
        bt.connect((id, ch))

        return bt