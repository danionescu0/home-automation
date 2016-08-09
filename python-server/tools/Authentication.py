class Authentication:
    AUTHENTICATION_COOKIE_NAME = 'user'
    def __init__(self, credentials):
        self.__credentials = credentials

    def verify_credentials(self, username, password):
        for i, user in enumerate(self.__credentials):
            if user['username'] == username and user['password'] == password:
                return True

        return False

    def verify_fingerprint_code(self, code):
        for i, user in enumerate(self.__credentials):
            if user['fingerprint_code'] == code:
                return True

        return False