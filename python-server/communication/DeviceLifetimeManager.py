from communication.DeviceLifetimeCycles import DeviceLifetimeCycles


class DeviceLifetimeManager(DeviceLifetimeCycles):
    def __init__(self) -> None:
        self.__devices = {}

    def connect(self):
        [device.connect() for name, device in self.__devices.items()]

    def disconnect(self) -> None:
        [device.disconnect() for name, device in self.__devices.items()]

    def add_device(self, name: str, device: DeviceLifetimeCycles):
        self.__devices[name] = device

        return self

    def get_device(self, name: str):
        return self.__devices[name]