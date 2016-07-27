import json
import logging
from tornado.web import  authenticated
from datetime import datetime, timedelta
from dateutil import tz
from web.BaseHandler import BaseHandler

class GraphsBuilderHandler(BaseHandler):
    def initialize(self, data_container):
        self.data_container = data_container

    @authenticated
    def get(self):
        data = self.__get_data_from_db('light', 1, None)
        self.render("../html/graphs.html",
                    datetimeList = json.dumps(data["datetime_list"]),
                    datapointValues = json.dumps(data["datapoint_values"]),
                    selectedType = type,
                    menuSelected ="graphs",
                    selectedDaysBehind =  1,
                    selectedGroupedByHours =  0
                    )

    @authenticated
    def post(self, *args, **kwargs):
        logging.debug(self.get_argument('type', 'light'))
        type = self.get_argument('type', 'light')
        group_by_hours = int(self.get_argument("group_by_hours", None, True))
        nr_days_behind = int(self.get_argument("nr_days_behind", None, True))
        if group_by_hours == 0:
            data = self.__get_data_from_db(type, nr_days_behind, None)
        else:
            data = self.__get_data_from_db(type, nr_days_behind, group_by_hours)

        self.render("../html/graphs.html",
                    datetimeList = json.dumps(data["datetime_list"]),
                    datapointValues = json.dumps(data["datapoint_values"]),
                    selectedType = type,
                    menuSelected ="graphs",
                    selectedDaysBehind =  nr_days_behind,
                    selectedGroupedByHours =  group_by_hours
                    )

    def __get_data_from_db(self, type, nr_days_behind, group_by_hours):
        start_date = datetime.today() - timedelta(days=nr_days_behind)
        end_date = datetime.today()
        data = self.data_container.get_sensor_values_in_interval(start_date, end_date, group_by_hours)
        datetime_list = []
        datapoint_values = []
        from_zone = tz.gettz('UTC')
        to_zone = tz.gettz('Europe/Bucharest')
        self.__last_value_by_senzor_type = {}

        for datapoint in data:
            initial_date = datetime.fromtimestamp(int(datapoint['timestamp'])).replace(tzinfo=from_zone)
            local_date = initial_date.astimezone(to_zone)
            datetime_text = local_date.strftime('%Y-%m-%d %H:%M:%S')
            datetime_list.append(datetime_text)
            datapoint_values.append(self.__compute_datapoint_value(datapoint, type))

        return {"datapoint_values": datapoint_values, "datetime_list" : datetime_list}

    def __compute_datapoint_value(self, datapoint, type):
        if type in datapoint.keys():
            self.__last_value_by_senzor_type[type] = datapoint[type]
            return  datapoint[type]
        elif type in self.__last_value_by_senzor_type.keys():
            return self.__last_value_by_senzor_type[type]

        return 0