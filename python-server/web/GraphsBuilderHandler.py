import json
from tornado.web import  authenticated
from datetime import datetime, timedelta
from dateutil import tz
from web.BaseHandler import BaseHandler

class GraphsBuilderHandler(BaseHandler):
    def initialize(self, sensors_repo):
        self.__sensors_repo = sensors_repo

    @authenticated
    def get(self):
        data = self.__get_formated_data('light', 1, None)
        self.render("../html/graphs.html",
                    datetimeList = json.dumps(data["datetime_list"]),
                    datapointValues = json.dumps(data["datapoint_values"]),
                    selectedType = type,
                    selected_menu_item ="graphs",
                    selectedDaysBehind =  1,
                    selectedGroupedByHours =  0
                    )

    @authenticated
    def post(self, *args, **kwargs):
        sensor_type = self.get_argument('type', 'light')
        group_by_hours = int(self.get_argument("group_by_hours", None, True))
        nr_days_behind = int(self.get_argument("nr_days_behind", None, True))
        if group_by_hours == 0:
            data = self.__get_formated_data(sensor_type, nr_days_behind, None)
        else:
            data = self.__get_formated_data(sensor_type, nr_days_behind, group_by_hours)

        self.render("../html/graphs.html",
                    datetimeList = json.dumps(data["datetime_list"]),
                    datapointValues = json.dumps(data["datapoint_values"]),
                    selectedType = sensor_type,
                    selected_menu_item ="graphs",
                    selectedDaysBehind =  nr_days_behind,
                    selectedGroupedByHours =  group_by_hours
                    )

    def __get_formated_data(self, sensor_type, nr_days_behind, group_by_hours):
        start_date = datetime.today() - timedelta(days=nr_days_behind)
        end_date = datetime.today()
        if group_by_hours is None:
            data = self.__sensors_repo.get_sensor_values_in_interval(start_date, end_date)
        else:
            data = self.__sensors_repo.get_hourly_sensor_values_in_interval(start_date, end_date)
        datetime_list = []
        datapoint_values = []
        from_zone = tz.gettz('UTC')
        to_zone = tz.gettz('Europe/Bucharest')
        self.__last_value_by_sensor_type = {}

        for datapoint in data:
            initial_date = datetime.fromtimestamp(int(datapoint['timestamp'])).replace(tzinfo=from_zone)
            local_date = initial_date.astimezone(to_zone)
            datetime_text = local_date.strftime('%Y-%m-%d %H:%M:%S')
            datetime_list.append(datetime_text)
            datapoint_values.append(self.__fill_missing_sensor_values(datapoint, sensor_type))

        return {"datapoint_values": datapoint_values, "datetime_list" : datetime_list}

    def __fill_missing_sensor_values(self, datapoint, sensor_type):
        if sensor_type in datapoint.keys():
            self.__last_value_by_sensor_type[sensor_type] = datapoint[sensor_type]
            return datapoint[sensor_type]
        elif type in self.__last_value_by_sensor_type.keys():
            return self.__last_value_by_sensor_type[sensor_type]

        return 0