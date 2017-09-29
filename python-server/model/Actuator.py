class Actuator:
    def __init__(self, name: str, state: bool, device_type: str) -> None:
        self.name = name
        self.state = state
        self.device_type = device_type
        self._type = None
        self._room = None
        self._strategy = None
        self._communicator = None
        self._send_to_device = None
        self._command = None
        self._encription = None

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, value : str):
        self._type = value

    @property
    def room(self):
        return self._room

    @room.setter
    def room(self, value : str):
        self._room = value

    @property
    def strategy(self):
        return self._strategy

    @strategy.setter
    def strategy(self, value):
        self._strategy = value

    @property
    def communicator(self):
        return self._communicator

    @communicator.setter
    def communicator(self, value):
        self._communicator = value

    @property
    def send_to_device(self):
        return self._send_to_device

    @send_to_device.setter
    def send_to_device(self, value):
        self._send_to_device = value

    @property
    def command(self):
        return self._command

    @command.setter
    def command(self, value):
        self._command = value

    @property
    def encription(self):
        return self._encription

    @encription.setter
    def encription(self, value):
        self._encription = value

    def __repr__(self) -> str:
        return "Actuator: name({0}), state({1}), device_type({2}), type({3}), room({4})," \
               " strategy({5}), communicator({6}), send_to_device({7}), command({8})," \
               " encription({9})".format(self.name, self.state, self.device_type, self._type
                                                          ,self._room, self._strategy, self._communicator,
                                                          self._send_to_device, self._command, self._encription)