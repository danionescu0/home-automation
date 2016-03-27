import bluetooth

class btConnections:
    def __init__(self, bedroomBtString, livingBtString, balconyString, holwayBtString, fingerprintBtString):
        self.bedroomBtString = bedroomBtString
        self.livingBtString = livingBtString
        self.balconyString = balconyString
        self.holwayBtString = holwayBtString
        self.fingerprintBtString = fingerprintBtString
        self.connectionMapping = {
            'bedroom':      self.bedroomBtString,
            'living':       self.livingBtString,
            'balcony':      self.balconyString,
            'holway':       self.holwayBtString,
            'fingerprint':  self.fingerprintBtString
        }

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


    def connectAllBt(self):
        self.btConnections = {
            'bedroom':      self.__connnectToBluetooth(self.bedroomBtString, 1),
            'living':       self.__connnectToBluetooth(self.livingBtString, 1),
            'balcony':      self.__connnectToBluetooth(self.balconyString, 1),
            'holway':       self.__connnectToBluetooth(self.holwayBtString, 1),
            'fingerprint':  self.__connnectToBluetooth(self.fingerprintBtString, 1)
        }

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