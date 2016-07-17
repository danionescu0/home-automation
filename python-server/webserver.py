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
import config

data_container = DataContainer(config.redisConfig)
locationTracker = LocationTracker(config.redisConfig)
job_controll = JobControll(config.redisConfig)

logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s] (%(threadName)-10s) %(message)s')
saveLocationListener = SaveLocationListener(locationTracker)
toggleAlarmFromLocationListener = ToggleAlarmFromLocationListener(config.homeCoordonates, job_controll, locationTracker)

def make_app():
    global config, data_container, job_controll

    settings = {
        "cookie_secret": "wellithinksecretisnice",
        "login_url": "/login",
    }

    return Application([
            url(
                r"/actuator/([a-zA-Z1-9]+)/(on|off)",
                ActuatorsHandler,
                dict(data_container=data_container, job_controll=job_controll),
                name="actuator-states"
            ),
            url(r'/login', LoginHandler, dict(credentials=config.credentials), name='login'),
            url(r'/public/(.*)', StaticFileHandler, {'path': config.staticPath}),
            url(r'/graphs', GraphsBuilderHandler, dict(data_container=data_container), name='graphs'),
            url(r'/time-rules', TimeRulesHandler, dict(data_container=data_container, logging=logging), name='timeRules'),
            url(
                r'/api/(.*)',
                ApiHandler,
                dict(data_container=data_container, credentials=config.credentials, logging=logging),
                name='api'
            ),
        ], **settings)

app = make_app()
app.listen(config.applicationPort)
IOLoop.current().start()
