from tornado.web import  authenticated
from web.BaseHandler import BaseHandler

class MainHandler(BaseHandler):
    def initialize(self, job_controll, actuators_repo, sensors_repo):
        self.job_controll = job_controll
        self.__actuators_repo = actuators_repo
        self.__sensors_repo = sensors_repo

    @authenticated
    def get(self):
        actuators = self.__actuators_repo.get_actuators()
        self.render(
            "./template/main.html",
            actuator_type_single = self.__filter_actuator_by_type(actuators, 'single'),
            actuator_type_bi = self.__group_actuators_by_type(self.__filter_actuator_by_type(actuators, 'bi')),
            sensors = self.__sensors_repo.get_sensors(),
            selected_menu_item="home"
        )

    @authenticated
    def post(self, *args, **kwargs):
        actuator_name = self.get_argument("actuator_name", None, True)
        actuator_value = self.get_argument("actuator_value", None, True)
        self.job_controll.change_actuator(actuator_name, {'false' : False, 'true': True}[actuator_value])

    def __filter_actuator_by_type(self, actuators, type):
        return {key: data for key, data in actuators.items() if actuators[key]['type'] == type}

    def __group_actuators_by_type(self, actuators):
        grouped_actuators = {}
        for actuator_name, actuator_properties in actuators.iteritems():
            group_key = actuator_properties['device_type']
            if not group_key in grouped_actuators:
                grouped_actuators[group_key] = []
            actuator_data = actuators[actuator_name]
            actuator_data['name'] = actuator_name
            grouped_actuators[group_key].append(actuator_data)

        return grouped_actuators