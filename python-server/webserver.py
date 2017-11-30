from tornado.ioloop import IOLoop
from tornado.web import Application, url, StaticFileHandler

from config import general

from web.ApiTokenAuthHandler import ApiTokenAuthHandler
from web.ApiLocationHandler import ApiLocationHandler
from web.ApiVoiceCommandHandler import ApiVoiceCommandHandler
from web.ApiRoomsHandler import ApiRoomsHandler
from web.ApiActuatorHandler import ApiActuatorHandler
from web.ApiActuatorsHandler import ApiActuatorsHandler
from web.ApiSensorHandler import ApiSensorHandler
from web.ApiIftttMultipleHandler import ApiIftttMultipleHandler
from web.ApiIftttSingleHandler import ApiIftttSingleHandler
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

    return Application([
            url(
                r'/api/user/token',
                ApiTokenAuthHandler,
                dict(authentication=authentication, jwt_token_factory=container.jwt_token_factory()),
                name='api_token_login'
            ),
            url(r'/api/location', ApiLocationHandler, name='api_location'),
            url(
                r'/api/voice-command',
                ApiVoiceCommandHandler,
                dict(voice_commands=container.voice_commands()),
                name='api_voice_command'
            ),
            url(
                r'/api/rooms', ApiRoomsHandler,
                dict(rooms_formatter=container.rooms_formatter()), name='api_rooms'
            ),
            url(
                r'/api/ifttt', ApiIftttMultipleHandler,
                dict(ifttt_formatter=container.ifttt_formatter()),
                name='api_rooms_multiple'
            ),
            url(
                r'/api/ifttt/(.*)', ApiIftttSingleHandler,
                dict(ifttt_rules_repository=container.ifttt_rules_repository(), rule_factory=container.rule_factory()),
                name='api_rooms_single'
            ),
            url(
                r'/api/actuator', ApiActuatorHandler,
                dict(async_actuator_commands=async_actuator_commands),
                name='api_actuator'
            ),
            url(
                r'/api/actuators', ApiActuatorsHandler,
                dict(actuators_formatter=container.actuators_formatter()),
                name='api_actuators'
            ),
            url(
                r'/api/sensor/(.*)', ApiSensorHandler,
                dict(sensors_formatter=container.sensors_formatter()),
                name='api_sensor'
            ),
            url(r'/(.*)', StaticFileHandler, {
                'path': general.web_server['static_path']
            }),
        ])

app = make_app()
app.listen(general.web_server['application_port'])
IOLoop.current().start()