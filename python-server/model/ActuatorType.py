from enum import Enum


class ActuatorType(Enum):
    PUSHBUTTON = 'pushbutton'
    SWITCH = 'switch'
    DIMMER = 'dimmer'