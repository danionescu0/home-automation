from datetime import datetime
from operator import itemgetter
from dateutil import tz

from tornado.web import authenticated
from typeguard import typechecked
from tools.DateUtils import DateUtils

from web.BaseHandler import BaseHandler
from repository.SensorsRepository import SensorsRepository


class SystemStatusHandler(BaseHandler):
    @typechecked()
    def initialize(self, sensors_repo: SensorsRepository):
        self.__sensors_repo = sensors_repo

    @authenticated
    def get(self):
        self.render(
            "./template/system-status.html",
            sensors_last_updated = self.__get_formated_data(),
            selected_menu_item="systemStatus"
        )

    def __get_formated_data(self):
        sensors = self.__sensors_repo.get_sensors()
        from_zone = tz.gettz('UTC')
        to_zone = tz.gettz(DateUtils.get_timezone())
        current_time = datetime.now(to_zone)
        sensors_list = []

        for sensor in sensors:
            initial_date = datetime.fromtimestamp(int(sensor.last_updated)).replace(tzinfo=from_zone)
            local_date = initial_date.astimezone(to_zone)
            datetime_text = local_date.strftime('%Y-%m-%d %H:%M:%S')
            sensors_list.append({
                'name': "{0}_{1}".format(sensor.type, sensor.location),
                'last_updated' : datetime_text,
                'minutes_since_updated' : int((current_time - local_date).seconds / 60)
            })

        return sorted(sensors_list, key=itemgetter('minutes_since_updated'), reverse=True)
