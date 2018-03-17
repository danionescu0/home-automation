from model.BaseDeviceProperties import BaseDeviceProperties


class ActuatorProperties(BaseDeviceProperties):
    COMMUNICATOR = 'communicator'
    SEND_TO_DEVICE = 'send_to_device'
    COMMAND = 'command'
    ENCRIPTION = 'encription'
    MAX_VALUE = 'max_value'
    GROUP_ACTUATORS = 'actuators'
    GROUP_FUTURE_STATE = 'future_state'
    SHORTCUT = 'shortcut'