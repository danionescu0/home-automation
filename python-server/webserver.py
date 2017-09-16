import sys

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
from tools.AsyncJobs import AsyncJobs
from tools.VoiceCommands import VoiceCommands
from tools.LoggingConfig import LoggingConfig
from web.MainHandler import MainHandler
from web.ApiTokenAuthHandler import ApiTokenHandler
from web.ApiLocationHandler import ApiLocationHandler
from web.GraphsBuilderHandler import GraphsBuilderHandler
from web.LoginHandler import LoginHandler
from web.LogoutHandler import LogoutHandler
from web.IftttHandler import IftttHandler
from web.SystemStatusHandler import SystemStatusHandler
from ifttt.ExpressionValidator import ExpressionValidator
from ifttt.parser.Tokenizer import Tokenizer

authentication = Authentication(general.credentials)
actuators_repo = Actuators(general.redis_config, actuators.conf)
sensors_repo = Sensors(general.redis_config, sensors.conf)
ifttt_rules = IftttRules(general.redis_config)
location_tracker = LocationTracker(general.redis_config)
async_jobs = AsyncJobs(general.redis_config)
async_jobs.connect()

logging_config = LoggingConfig(general.logging['log_file'], general.logging['log_entries'])
logging = logging_config.get_logger()
sys.excepthook = logging_config.set_error_hadler

e1 = SaveLocationListener(location_tracker)
e2 = SetPhoneIsHomeListener(general.home_coordonates, sensors_repo, location_tracker)
tokenizer = Tokenizer(sensors_repo, actuators_repo)
ifttt_expression_validator = ExpressionValidator(tokenizer)
voice_commands = VoiceCommands(async_jobs, logging).configure()

def make_app():
    settings = {
        'cookie_secret': general.web_server['cookie_secret'],
        'login_url': '/login',
    }

    return Application([
            url(
                r"/",
                MainHandler,
                dict(job_controll=async_jobs, actuators_repo=actuators_repo, sensors_repo=sensors_repo),
                name="actuator-states"
            ),
            url(r'/login', LoginHandler, dict(authentication=authentication), name='login'),
            url(r'/public/(.*)', StaticFileHandler, {
                'path': general.web_server['static_path']
            }),
            url(r'/graphs', GraphsBuilderHandler, dict(
                sensors_repo=sensors_repo,
                sensors_config=sensors.conf
            ), name='graphs'),
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
                r'/api/user/token',
                ApiTokenHandler,
                dict(
                    authentication=authentication,
                    api_token_secret=general.web_server['api_token_secret']
                ),
                name='api_token_login'
            ),
            url(
                r'/api/location',
                ApiLocationHandler,
                dict(
                    api_token_secret=general.web_server['api_token_secret']
                ),
                name='api_location'
            ),
            url(
                r'/system-status',
                SystemStatusHandler,
                dict(sensors_repo=sensors_repo,),
                name='systemStatus'
            ),
            url(r'/logout', LogoutHandler, name='logout')
        ], **settings)

app = make_app()
app.listen(general.web_server['application_port'])
IOLoop.current().start()