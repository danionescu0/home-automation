import bluetooth

class btConnections:
    def __init__(self, connectionMapping):
        self.connectionMapping = connectionMapping
        self.btConnections = {}

    def sendToBluetooth(self, which, value):
        try:
            self.btConnections[which].send(value)
        except bluetooth.btcommon.BluetoothError as error:
            return self.__reconnectBluetooth(which)

        return True

    def reciveFromBluetooth(self, which, howMuch):
        try:
            return self.btConnections[which].recv(howMuch)
        except bluetooth.btcommon.BluetoothError as error:
            self.__reconnectBluetooth(which)

        return False


    def connect(self):
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