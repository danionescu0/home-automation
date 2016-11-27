import jwt
from dateutil.relativedelta import relativedelta
import datetime, time

from web.BaseHandler import BaseHandler
from event.LocationEvent import LocationEvent

class ApiHandler(BaseHandler):
    def initialize(self, authentication, api_token_secret, voice_commands, logging):
        self.__authentication = authentication
        self.__api_token_secret = api_token_secret
        self.__voice_commands = voice_commands
        self.logging = logging

    def get(self, module):
        if module == 'record-location':
            success = self.record_location()
        elif module == 'token-auth':
            success = self.token_auth()
        elif module == 'voice-command':
            success = self.execute_command()
        else:
            self.set_status(404)
            self.write({'status': False, 'error': 'not implemented'})
        if not success:
            self.set_status(500)
            self.write({'status': False, 'error': 'bad credentials'})

    # @ToDo refactored duplicate code with record_location
    def execute_command(self):
        username = self.__check_token()
        if not username:
            return False
        command = self.get_argument('command', None, True)
        self.__voice_commands.execute(command)
        self.write({'status': True})

        return True

    def record_location(self):
        username = self.__check_token()
        if not username:
            return False
        latitude = float(self.get_argument('latitude', None, True))
        longitude = float(self.get_argument('longitude', None, True))
        location_event = LocationEvent()
        location_event.send(username, latitude, longitude)
        self.write({'status': True})

        return True

    def token_auth(self):
        username = self.get_argument('username', None, True)
        password = self.get_argument('password', None, True)
        if (not self.__authentication.verify_credentials(username, password)):
            return False

        expire = datetime.date.today() + relativedelta(months=1)
        jwt_data = {'sub' : username, 'exp': time.mktime(expire.timetuple())}
        token = jwt.encode(jwt_data, self.__api_token_secret, algorithm='HS256')
        self.write(token)

        return True

    def __check_token(self):
        auth_header = self.request.headers.get("Authorization")
        if not auth_header:
            return False
        auth_header = auth_header.split()
        if auth_header[0] != 'Bearer':
            return False
        decoded_token_data = jwt.decode(auth_header[1], self.__api_token_secret, algorithm='HS256')

        return decoded_token_data['sub']
