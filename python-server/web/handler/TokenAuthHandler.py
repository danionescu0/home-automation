from typeguard import typechecked

from tools.Authentication import Authentication
from web.handler.CorsHandler import CorsHandler
from web.security.JwtTokenFactory import JwtTokenFactory


class TokenAuthHandler(CorsHandler):
    @typechecked()
    def initialize(self, authentication: Authentication, jwt_token_factory: JwtTokenFactory):
        self.__authentication = authentication
        self.__jwt_token_factory = jwt_token_factory

    def post(self):
        username = self.get_argument('username', None, True)
        password = self.get_argument('password', None, True)
        if (not self.__authentication.verify_credentials(username, password)):
            self.set_status(500)
            self.write({'status': False, 'error': 'bad credentials'})
        self.write(self.__jwt_token_factory.create(username))