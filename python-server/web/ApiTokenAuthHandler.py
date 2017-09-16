import datetime, time
from dateutil.relativedelta import relativedelta

from typeguard import typechecked
import jwt

from web.BaseHandler import BaseHandler
from tools.Authentication import Authentication


class ApiTokenHandler(BaseHandler):
    @typechecked()
    def initialize(self, authentication: Authentication, api_token_secret: str):
        self.__authentication = authentication
        self.api_token_secret = api_token_secret

    def post(self):
        print(self.request.body)
        username = self.get_argument('username', None, True)
        password = self.get_argument('password', None, True)
        if (not self.__authentication.verify_credentials(username, password)):
            self.set_status(500)
            self.write({'status': False, 'error': 'bad credentials'})

        expire = datetime.date.today() + relativedelta(months=1)
        jwt_data = {
            'sub' : username,
            'exp': time.mktime(expire.timetuple())
        }
        token = jwt.encode(jwt_data, self.api_token_secret, algorithm='HS256')
        self.write(token)