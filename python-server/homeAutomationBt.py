import bluetooth

class btConnections:
    def __init__(self, bedroomBtString, livingBtString):
        self.bedroomBtString = bedroomBtString
        self.livingBtString = livingBtString

    def connnectToBluetooth(self, id, ch):
        bt = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        bt.settimeout(None)
        bt.connect((id, ch))

        return bt

    def connectAllBt(self):
        return {
            'bedroom': self.connnectToBluetooth(self.bedroomBtString, 1),
            'living': self.connnectToBluetooth(self.livingBtString, 1)
        }