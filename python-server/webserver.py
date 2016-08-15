import logging

from tornado.ioloop import IOLoop
from tornado.web import Application, url, StaticFileHandler

from config import actuators
from config import configuration
from listener.SaveLocationListener import SaveLocationListener
from listener.ToggleAlarmFromLocationListener import ToggleAlarmFromLocationListener
from repository.DataContainer import DataContainer
from repository.LocationTracker import LocationTracker
from repository.TimeRules import TimeRules
from tools.Authentication import Authentication
from tools.JobControl import JobControll
from web.ActuatorsHandler import ActuatorsHandler
from web.ApiHandler import ApiHandler
from web.GraphsBuilderHandler import GraphsBuilderHandler
from web.LoginHandler import LoginHandler
from web.LogoutHandler import LogoutHandler
from web.TimeRulesHandler import TimeRulesHandler

authentication = Authentication(configuration.credentials)
data_container = DataContainer(configuration.redis_config, actuators.conf)
time_rules = TimeRules(configuration.redis_config)
location_tracker = LocationTracker(configuration.redis_config)
job_controll = JobControll(configuration.redis_config)

logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s] (%(threadName)-10s) %(message)s')
saveLocationListener = SaveLocationListener(location_tracker)
toggle_alarm_from_location_listener = ToggleAlarmFromLocationListener(configuration.home_coordonates, job_controll, location_tracker)

def make_app():
    global configuration, data_container, job_controll

    settings = {
        'cookie_secret': configuration.web_server['cookie_secret'],
        'login_url': '/login',
    }

    return Application([
            url(
                r"/actuator/([a-zA-Z1-9]+)/(on|off)|/actuators",
                ActuatorsHandler,
                dict(data_container=data_container, job_controll=job_controll),
                name="actuator-states"
            ),
            url(r'/login', LoginHandler, dict(authentication = authentication), name='login'),
            url(r'/public/(.*)', StaticFileHandler, {
                'path': configuration.web_server['static_path']
            }),
            url(r'/graphs', GraphsBuilderHandler, dict(data_container=data_container), name='graphs'),
            url(r'/time-rules',
                TimeRulesHandler,
                dict(
                    data_container=data_container,
                    time_rules=time_rules,
                    logging=logging
                ),
                name='timeRules'),
            url(
                r'/api/(.*)',
                ApiHandler,
                dict(
                    data_container=data_container,
                    authentication=authentication,
                    logging=logging
                ),
                name='api'
            ),
            url(r'/logout', LogoutHandler, name='logout')
        ], **settings)

app = make_app()
app.listen(configuration.web_server['application_port'])
IOLoop.current().start()