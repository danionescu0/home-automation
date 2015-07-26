import bluetooth

bt2 = "20:14:12:08:20:45"
bt1 = "00:14:01:13:16:44"

def connnectToBluetooth(id, ch):
    bt = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    bt.settimeout(None)
    bt.connect((id, ch))

    return bt

def connectAllBt():

    return {
        'bedroom': connnectToBluetooth(bt1, 1),
        'sensors': connnectToBluetooth(bt2, 1)
    }