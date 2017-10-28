from communication.DeviceLifetimeCycles import DeviceLifetimeCycles


class DeviceLifetimeManager(DeviceLifetimeCycles):
    def __init__(self) -> None:
        self.__devices = []

    def connect(self):
        [device.connect() for device in self.__devices]

    def disconnect(self) -> None:
        [device.disconnect() for device in self.__devices]

    def add_device(self, device: DeviceLifetimeCycles):
        self.__devices.append(device)

        return self