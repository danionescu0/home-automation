import abc

from typeguard import typechecked

from model.configuration.BaseConfig import BaseConfig


class EmailCfg(BaseConfig, metaclass=abc.ABCMeta):
    @typechecked()
    def __init__(self, sender_address: str, password: str) -> None:
        self.sender_address = sender_address
        self.password = password
        super(EmailCfg, self).__init__()

    @typechecked()
    def main_description(self) -> str:
        return 'Email settings (gmail account that is used to send emails)'

    @typechecked()
    def properties_description(self) -> dict:
        return {
            'sender_address' : 'Sender address, ex: test@gmail.com',
            'password': "Password: your password for the email account"
        }