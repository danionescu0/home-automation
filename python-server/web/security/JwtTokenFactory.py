from datetime import datetime
from datetime import timedelta

import jwt

class JwtTokenFactory:
    def __init__(self, secret: str) -> None:
        self.__secret = secret

    def create(self, id: str) -> str:
        payload = {
            'sub': id,
            'exp': datetime.utcnow() + timedelta(days=1)
        }

        return jwt.encode(payload, self.__secret, algorithm='HS256')