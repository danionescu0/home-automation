import logging

from tornado.ioloop import IOLoop
from tornado.web import Application, url, StaticFileHandler

from listener.SaveLocationListener import SaveLocationListener
from listener.ToggleAlarmFromLocationListener import ToggleAlarmFromLocationListener
from tools.DataContainer import DataContainer
from tools.JobControl import JobControll
from tools.LocationTracker import LocationTracker
from web.ActuatorsHandler import ActuatorsHandler
from web.ApiHandler import ApiHandler
from web.GraphsBuilderHandler import GraphsBuilderHandler
from web.LoginHandler import LoginHandler
from web.TimeRulesHandler import TimeRulesHandler
import configuration

data_container = DataContainer(configuration.redis_config)
locationTracker = LocationTracker(configuration.redis_config)
job_controll = JobControll(configuration.redis_config)

logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s] (%(threadName)-10s) %(message)s')
saveLocationListener = SaveLocationListener(locationTracker)
toggleAlarmFromLocationListener = ToggleAlarmFromLocationListener(configuration.home_coordonates, job_controll, locationTracker)

def make_app():
    global configuration, data_container, job_controll

    settings = {
        'cookie_secret': configuration.web_server['cookie_secret'],
        'login_url': '/login',
    }

    return Application([
            url(
                r"/actuator/([a-zA-Z1-9]+)/(on|off)",
                ActuatorsHandler,
                dict(data_container=data_container, job_controll=job_controll),
                name="actuator-states"
            ),
            url(r'/login', LoginHandler, dict(credentials=configuration.credentials), name='login'),
            url(r'/public/(.*)', StaticFileHandler, {
                'path': configuration.web_server['static_path']
            }),
            url(r'/graphs', GraphsBuilderHandler, dict(data_container=data_container), name='graphs'),
            url(r'/time-rules', TimeRulesHandler, dict(data_container=data_container, logging=logging), name='timeRules'),
            url(
                r'/api/(.*)',
                ApiHandler,
                dict(data_container=data_container, credentials=configuration.credentials, logging=logging),
                name='api'
            ),
        ], **settings)

app = make_app()
app.listen(configuration.web_server['application_port'])
IOLoop.current().start()
