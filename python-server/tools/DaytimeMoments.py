import datetime

from pytz import timezone
from astral import Astral

class DaytimeMoments:
    @staticmethod
    def is_over_sunset():
        astral = Astral()
        astral.solar_depression = 'civil'
        sun = astral['Bucharest'].sun(date=datetime.datetime.now(), local=True)
        currentTime = datetime.datetime.now(timezone('Europe/Bucharest')).time()

        return currentTime > sun['sunset'].time()