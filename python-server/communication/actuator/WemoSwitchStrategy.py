from BaseStrategy import BaseStrategy
from ouimeaux.environment import Environment

class WemoSwitchStrategy(BaseStrategy):

    def __init__(self, actuators_config):
        super(WemoSwitchStrategy, self).__init__(actuators_config)

    def supports(self, actuator_name):
        return self.actuators_config[actuator_name]['strategy'] == 'wemo-switch'

    def toggle(self, actuator_name, state):
        env = Environment()
        env.start()
        env.discover(seconds=1)
        switch = env.get_switch(self.actuators_config[actuator_name]['send_to_device'])
        if (state):
            switch.on()
        else:
            switch.off()
