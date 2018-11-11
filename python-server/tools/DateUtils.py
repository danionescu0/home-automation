import datetime

from astral import Astral
from pytz import timezone
from typeguard import typechecked

import config


class DateUtils:
    @staticmethod
    @typechecked()
    def is_over_sunset() -> bool:
        astral = Astral()
        astral.solar_depression = 'civil'
        sun = astral['Bucharest'].sun(date=datetime.datetime.now(), local=True)
        currentTime = datetime.datetime.now(timezone(config.timezone)).time()

        return currentTime > sun['sunset'].time()

    @staticmethod
    @typechecked()
    def get_timezone() -> str:
        return config.timezone