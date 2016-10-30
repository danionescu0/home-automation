import json
from tornado.web import  authenticated
from datetime import datetime, timedelta
from dateutil import tz
from web.BaseHandler import BaseHandler

class GraphsBuilderHandler(BaseHandler):
    def initialize(self, sensors_repo, sensors_config):
        self.__sensors_repo = sensors_repo
        self.__sensors_config = sensors_config

    @authenticated
    def get(self):
        data = self.__get_formated_data('light', 'living', 1, None)
        self.render("./template/graphs.html",
                    datetimeList = json.dumps(data["datetime_list"]),
                    datapointValues = json.dumps(data["datapoint_values"]),
                    selected_sensor = self.__get_selected_sensor_data(),
                    sensors_config = self.__sensors_config,
                    selected_menu_item ="graphs",
                    selectedDaysBehind =  1,
                    selectedGroupedByHours =  0
                    )

    # @authenticated
    def post(self, *args, **kwargs):
        print json.dumps({ k: self.get_argument(k) for k in self.request.arguments })
        selected_sensor = self.__get_selected_sensor_data()
        group_by_hours = int(self.get_argument("group_by_hours", None, True))
        nr_days_behind = int(self.get_argument("nr_days_behind", None, True))
        if group_by_hours == 0:
            data = self.__get_formated_data(selected_sensor['type'], selected_sensor['location'], nr_days_behind, None)
        else:
            data = self.__get_formated_data(selected_sensor['type'], selected_sensor['location'], nr_days_behind, group_by_hours)

        self.render("./template/graphs.html",
                    datetimeList = json.dumps(data["datetime_list"]),
                    datapointValues = json.dumps(data["datapoint_values"]),
                    selected_sensor = self.__get_selected_sensor_data(),
                    sensors_config=self.__sensors_config,
                    selected_menu_item ="graphs",
                    selectedDaysBehind =  nr_days_behind,
                    selectedGroupedByHours =  group_by_hours
                    )

    def __get_formated_data(self, sensor_type, sensor_location, nr_days_behind, group_by_hours):
        start_date = datetime.today() - timedelta(days=nr_days_behind)
        end_date = datetime.today()
        if group_by_hours is None:
            data = self.__sensors_repo.get_sensor_values_in_interval(sensor_type, sensor_location, start_date, end_date)
        else:
            data = self.__sensors_repo.get_hourly_sensor_values_in_interval(sensor_type, sensor_location, start_date, end_date)
        datetime_list = []
        datapoint_values = []
        from_zone = tz.gettz('UTC')
        to_zone = tz.gettz('Europe/Bucharest')

        for datapoint in data:
            initial_date = datetime.fromtimestamp(int(datapoint['timestamp'])).replace(tzinfo=from_zone)
            local_date = initial_date.astimezone(to_zone)
            datetime_text = local_date.strftime('%Y-%m-%d %H:%M:%S')
            datetime_list.append(datetime_text)
            datapoint_values.append(datapoint['value'])

        return {"datapoint_values": datapoint_values, "datetime_list" : datetime_list}


    def __get_selected_sensor_data(self):
        selected = self.get_argument('sensor', 'light:living')
        sensor_data = selected.split(':')

        return {
            'type' : sensor_data[0],
            'location' : sensor_data[1]
        }
