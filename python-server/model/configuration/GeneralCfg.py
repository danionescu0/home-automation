from typing import Tuple
import abc

from typeguard import typechecked

from model.configuration.BaseConfig import BaseConfig


class GeneralCfg(BaseConfig, metaclass=abc.ABCMeta):
    @typechecked()
    def __init__(self, home_coordonates: Tuple, aes_key: str) -> None:
        self.home_coordonates = home_coordonates
        self.aes_key = aes_key
        super(GeneralCfg, self).__init__()

    @typechecked()
    def main_description(self) -> str:
        return 'General configuration settings'

    @typechecked()
    def properties_description(self) -> dict:
        return {
            'home_coordonates' : 'A touple representing latitude and longitude with your home, '
                                 'example: (22.4169649, 35.1542889)',
            'aes_key': "Aes key used for encripted serial communication between arduino devices and HC-12 on "
                       "the serial port"
        }