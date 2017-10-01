import abc


class TokenConverter(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get_value(self, token_raw_value: str):
        pass

    @abc.abstractmethod
    def get_supported_token(self) -> str:
        pass