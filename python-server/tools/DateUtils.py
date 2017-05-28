import datetime
from pytz import timezone
from astral import Astral
from typeguard import typechecked

from config import general

class DateUtils:
    @staticmethod
    @typechecked()
    def is_over_sunset() -> bool:
        astral = Astral()
        astral.solar_depression = 'civil'
        sun = astral['Bucharest'].sun(date=datetime.datetime.now(), local=True)
        currentTime = datetime.datetime.now(timezone(general.timezone)).time()

        return currentTime > sun['sunset'].time()

    @staticmethod
    @typechecked()
    def get_timezone() -> str:
        return general.timezone