from datetime import datetime
from dateutil import tz

from ifttt.parser.TokenConverter import TokenConverter
from ifttt.parser.Token import Token
from tools.DateUtils import DateUtils


class CurrentTimeTokenConverter(TokenConverter):
    def get_value(self, token_raw_value: str):
        from_zone = tz.gettz('UTC')
        to_zone = tz.gettz(DateUtils.get_timezone())
        initial_date = datetime.now().replace(tzinfo=from_zone)
        local_date = initial_date.astimezone(to_zone)

        return local_date.strftime('%H:%M')

    def get_supported_token(self) -> str:
        return Token.TYPE_CURRENT_TIME