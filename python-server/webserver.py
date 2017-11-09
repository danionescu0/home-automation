from tornado.ioloop import IOLoop
from tornado.web import Application, url, StaticFileHandler

from config import general
from config import sensors

from web.MainHandler import MainHandler
from web.ApiTokenAuthHandler import ApiTokenAuthHandler
from web.ApiLocationHandler import ApiLocationHandler
from web.ApiVoiceCommandHandler import ApiVoiceCommandHandler
from web.ApiRoomsHandler import ApiRoomsHandler
from web.ApiActuatorHandler import ApiActuatorHandler
from web.GraphsBuilderHandler import GraphsBuilderHandler
from web.LoginHandler import LoginHandler
from web.LogoutHandler import LogoutHandler
from web.IftttHandler import IftttHandler
from web.SystemStatusHandler import SystemStatusHandler
from container import Container

container = Container()

root_logger = container.root_logger()
authentication = container.authentication()
actuators_repo = container.actuators_repository()
sensors_repo = container.sensors_repository()
async_actuator_commands = container.async_actuator_commands()
root_logger = container.root_logger()


save_location_listener = container.save_location_listener()
set_phone_is_home_listener = container.set_phone_is_home_listener()
async_actuator_commands.connect()


def make_app():
    settings = {
        'cookie_secret': general.web_server['cookie_secret'],
        'login_url': '/login',
    }

    return Application([
            url(
                r"/",
                MainHandler,
                dict(async_actuator_commands=async_actuator_commands, actuators_repo=actuators_repo, sensors_repo=sensors_repo),
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
                    rules_repository=container.ifttt_rules_repository(),
                    expression_validator=container.expression_validator(),
                ),
                name='ifttt'
                ),
            url(
                r'/system-status',
                SystemStatusHandler,
                dict(sensors_repo=sensors_repo),
                name='systemStatus'
            ),
            url(r'/logout', LogoutHandler, name='logout'),
            url(
                r'/api/user/token',
                ApiTokenAuthHandler,
                dict(authentication=authentication, jwt_token_factory=container.jwt_token_factory()),
                name='api_token_login'
            ),
            url(
                r'/api/location',
                ApiLocationHandler,
                name='api_location'
            ),
            url(
                r'/api/voice-command',
                ApiVoiceCommandHandler,
                dict(voice_commands=container.voice_commands()),
                name='api_voice_command'
            ),
            url(
                r'/api/rooms',
                ApiRoomsHandler,
                dict(rooms_formatter=container.rooms_formatter()),
                name='api_rooms'
            ),
            url(
                r'/api/actuator',
                ApiActuatorHandler,
                dict(async_actuator_commands=async_actuator_commands),
                name='api_actuator'
            )
        ], **settings)

app = make_app()
app.listen(general.web_server['application_port'])
IOLoop.current().start()