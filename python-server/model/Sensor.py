from typing import Tuple

class Sensor:
    def __init__(self, id: str, type: str, location: str, value) -> None:
        self.id = id
        self.type = type
        self.location = location
        self.value = value
        self._visible = None
        self._communication_code = None
        self._last_updated = None

    @property
    def visible(self):
        return self._visible

    @visible.setter
    def visible(self, state : bool):
        self._visible = state

    @property
    def communication_code(self) -> Tuple:
        return self._communication_code

    @communication_code.setter
    def communication_code(self, value: Tuple):
        self._communication_code = value

    @property
    def last_updated(self):
        return self._last_updated

    @last_updated.setter
    def last_updated(self, value):
        self._last_updated = value

    def __repr__(self) -> str:
        return "Sensor: type({0}), location({1}), value({2}), visible({3})," \
               " communication_code({4}), last_updated({5})".format(self.type, self.location, self.value,
                                                                    self._visible, self._communication_code,
                                                                    self._last_updated)