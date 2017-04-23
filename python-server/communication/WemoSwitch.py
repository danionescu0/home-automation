from .Base import Base
from ouimeaux.environment import Environment
from ouimeaux.environment import UnknownDevice

class WemoSwitch(Base):
    def send(self, which, value):
        env = Environment()
        try:
            env.start()
            env.discover(seconds=1)
            switch = env.get_switch(which)
            if (value):
                switch.on()
            else:
                switch.off()
        except UnknownDevice:
            return False

        return True

    def connect(self):
        pass

    def disconnect(self):
        pass

    def listen(self, complete_message_callback, receive_message_callback):
        pass