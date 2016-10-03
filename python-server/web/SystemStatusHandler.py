from tornado.web import  authenticated
from datetime import datetime, timedelta
from dateutil import tz
from web.BaseHandler import BaseHandler

class SystemStatusHandler(BaseHandler):
    def initialize(self,  sensors_repo):
        self.__sensors_repo = sensors_repo

    @authenticated
    def get(self):
        self.render(
            "./template/system-status.html",
            sensors_last_updated = self.__get_formated_data(),
            selected_menu_item="systemStatus"
        )

    def __get_formated_data(self):
        data = self.__sensors_repo.get_sensors()
        from_zone = tz.gettz('UTC')
        to_zone = tz.gettz('Europe/Bucharest')
        sensors_list = []

        for datapoint in data:
            initial_date = datetime.fromtimestamp(int(datapoint['last_updated'])).replace(tzinfo=from_zone)
            local_date = initial_date.astimezone(to_zone)
            datetime_text = local_date.strftime('%Y-%m-%d %H:%M:%S')
            sensors_list.append({
                'name': "{0}_{1}".format(datapoint['type'], datapoint['location']),
                'last_updated' : datetime_text
            })
        print sensors_list

        return sensors_list
