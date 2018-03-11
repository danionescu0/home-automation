from datetime import datetime
from datetime import timedelta

import jwt
from typeguard import typechecked


class JwtTokenFactory:
    @typechecked()
    def __init__(self, secret: str, token_validity_days: int) -> None:
        self.__secret = secret
        self.__token_validity_days = token_validity_days

    @typechecked()
    def create(self, id: str) -> str:
        payload = {
            'sub': id,
            'exp': datetime.utcnow() + timedelta(days=self.__token_validity_days)
        }

        return jwt.encode(payload, self.__secret, algorithm='HS256')