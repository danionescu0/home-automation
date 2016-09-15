import logging

from tornado.ioloop import IOLoop
from tornado.web import Application, url, StaticFileHandler

from config import actuators
from config import general
from config import sensors
from listener.SaveLocationListener import SaveLocationListener
from listener.SetPhoneIsHomeListener import SetPhoneIsHomeListener
from repository.LocationTracker import LocationTracker
from repository.IftttRules import IftttRules
from repository.Actuators import Actuators
from repository.Sensors import Sensors
from tools.Authentication import Authentication
from tools.JobControl import JobControll
from web.MainHandler import MainHandler
from web.ApiHandler import ApiHandler
from web.GraphsBuilderHandler import GraphsBuilderHandler
from web.LoginHandler import LoginHandler
from web.LogoutHandler import LogoutHandler
from web.IftttHandler import IftttHandler
from ifttt.ExpressionValidator import ExpressionValidator

authentication = Authentication(general.credentials)
actuators_repo = Actuators(general.redis_config, actuators.conf)
sensors_repo = Sensors(general.redis_config, sensors.conf)
ifttt_rules = IftttRules(general.redis_config)
location_tracker = LocationTracker(general.redis_config)
job_controll = JobControll(general.redis_config)

logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s] (%(threadName)-10s) %(message)s')
saveLocationListener = SaveLocationListener(location_tracker)
set_phone_is_home_listener = SetPhoneIsHomeListener(general.home_coordonates, sensors_repo, location_tracker)
ifttt_expression_validator = ExpressionValidator(sensors_repo, actuators_repo)

def make_app():
    settings = {
        'cookie_secret': general.web_server['cookie_secret'],
        'login_url': '/login',
    }

    return Application([
            url(
                r"/actuator/([a-zA-Z1-9]+)/(on|off)|/",
                MainHandler,
                dict(job_controll=job_controll, actuators_repo = actuators_repo, sensors_repo = sensors_repo),
                name="actuator-states"
            ),
            url(r'/login', LoginHandler, dict(authentication = authentication), name='login'),
            url(r'/public/(.*)', StaticFileHandler, {
                'path': general.web_server['static_path']
            }),
            url(r'/graphs', GraphsBuilderHandler, dict(sensors_repo=sensors_repo), name='graphs'),
            url(r'/ifttt',
                IftttHandler,
                dict(
                    actuators_repo=actuators_repo,
                    ifttt_rules=ifttt_rules,
                    ifttt_expression_validator=ifttt_expression_validator,
                    logging=logging
                ),
                name='ifttt'),
            url(
                r'/api/(.*)',
                ApiHandler,
                dict(
                    authentication=authentication,
                    api_token_secret = general.web_server['api_token_secret'],
                    logging=logging
                ),
                name='api'
            ),
            url(r'/logout', LogoutHandler, name='logout')
        ], **settings)

app = make_app()
app.listen(general.web_server['application_port'])
IOLoop.current().start()