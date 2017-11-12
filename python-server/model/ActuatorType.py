from enum import Enum


class ActuatorType(Enum):
    PUSHBUTTON = 'single'
    SWITCH = 'bi'
    DIMMER = 'dimmer'