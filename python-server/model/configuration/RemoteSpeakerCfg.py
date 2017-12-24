import abc

from typeguard import typechecked

from model.configuration.BaseConfig import BaseConfig


class RemoteSpeakerCfg(BaseConfig, metaclass=abc.ABCMeta):
    @typechecked()
    def __init__(self, host: str, user: str, password: str) -> None:
        self.host = host
        self.user = user
        self.password = password

    @typechecked()
    def main_description(self) -> str:
        return 'Remote speaker configuration'

    @typechecked()
    def properties_description(self) -> dict:
        return {
            'host' : 'Hostname',
            'user' : 'Username',
            'password': "Password"
        }