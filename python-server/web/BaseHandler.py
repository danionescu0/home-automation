import jwt
from tornado.web import RequestHandler


class BaseHandler(RequestHandler):
    def render(self, template, **kwargs):
        kwargs['username'] = self.get_secure_cookie("user")
        super(BaseHandler, self).render(template, **kwargs)

    def get_current_user(self):
        return self.get_secure_cookie("user")

    def check_token(self):
        auth_header = self.request.headers.get("Authorization")
        if not auth_header:
            return False
        auth_header = auth_header.split()
        if auth_header[0] != 'Bearer':
            return False
        decoded_token_data = jwt.decode(auth_header[1], self.api_token_secret, algorithm='HS256')

        return decoded_token_data['sub']