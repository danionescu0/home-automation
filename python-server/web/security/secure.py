import jwt

from config import general


def secure(method):
    def wrapper(self, *args, **kwargs):
        auth = self.request.headers.get('Authorization')
        if not auth:
            return invalid_auth(self, "Missing authorization")

        auth_header = auth.split()

        if auth_header[0].lower() != 'bearer' or len(auth_header) == 1:
            return invalid_auth(self, "Invalid authorization header")
        token = auth_header[1]
        try:
            jwt.decode(token, general.web_server['api_token_secret'], algorithm='HS256')
        except Exception as e:
            invalid_auth(self, "Invalid token")

        return method(self, *args, **kwargs)

    def invalid_auth(self, message):
        self.set_status(401)
        self.write(message)
        self.finish()

    return wrapper