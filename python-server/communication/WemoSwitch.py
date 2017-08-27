from typing import Callable

from typeguard import typechecked
from ouimeaux.environment import Environment
from ouimeaux.environment import UnknownDevice

from .Base import Base


class WemoSwitch(Base):

    @typechecked()
    def send(self, which: str, value: bytes):
        env = Environment()
        try:
            env.start()
            env.discover(seconds=1)
            switch = env.get_switch(which)
            if (value.decode('utf-8') == 'True'):
                switch.on()
            else:
                switch.off()
        except UnknownDevice:
            return False

        return True

    def connect(self):
        pass

    @typechecked()
    def disconnect(self) -> None:
        pass

    @typechecked()
    def listen(self, complete_message_callback: Callable[[str], bool], receive_message_callback: Callable[[str], None]):
        pass