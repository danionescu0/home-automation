from BaseStrategy import BaseStrategy

class GroupStrategy(BaseStrategy):
    def __init__(self, actuators_config, job_controll):
        super(GroupStrategy, self).__init__(actuators_config)
        self.__job_controll = job_controll

    def supports(self, actuator_name):
        return self.actuators_config[actuator_name]['strategy'] == 'group'

    def toggle(self, actuator_name, state):
        toggle_actuators = self.actuators_config[actuator_name]['actuators']
        future_state = self.actuators_config[actuator_name]['futureState']
        for actuator_name in toggle_actuators:
            self.__job_controll.change_actuator(actuator_name, future_state)

        return True