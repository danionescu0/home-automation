from typeguard import typechecked

class Authentication:
    AUTHENTICATION_COOKIE_NAME = 'user'

    @typechecked()
    def __init__(self, credentials: list):
        self.__credentials = credentials

    @typechecked()
    def verify_credentials(self, username: str, password: str) -> bool:
        for i, user in enumerate(self.__credentials):
            if user['username'] == username and user['password'] == password:
                return True

        return False

    @typechecked()
    def verify_fingerprint_code(self, code: str) -> bool:
        for i, user in enumerate(self.__credentials):
            if user['fingerprint_code'] == code:
                return True

        return False