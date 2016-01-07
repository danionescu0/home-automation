import bluetooth

class btConnections:
    def __init__(self, bedroomBtString, livingBtString, balconyString, holwayBtString):
        self.bedroomBtString = bedroomBtString
        self.livingBtString = livingBtString
        self.balconyString = balconyString
        self.holwayBtString = holwayBtString

    def connnectToBluetooth(self, id, ch):
        bt = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        bt.settimeout(None)
        bt.connect((id, ch))

        return bt

    def connectAllBt(self):
        return {
            'bedroom':   self.connnectToBluetooth(self.bedroomBtString, 1),
            'living':    self.connnectToBluetooth(self.livingBtString, 1),
            'balcony':   self.connnectToBluetooth(self.balconyString, 1),
            'holway':     self.connnectToBluetooth(self.holwayBtString, 1)
        }