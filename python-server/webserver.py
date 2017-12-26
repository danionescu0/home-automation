from tornado.ioloop import IOLoop
from tornado.web import Application, url, StaticFileHandler

from config import general
from container import Container
from web.handler.ActuatorHandler import ActuatorHandler
from web.handler.ActuatorsHandler import ActuatorsHandler
from web.handler.IftttHandler import IftttHandler
from web.handler.IftttListHandler import IftttListHandler
from web.handler.LocationHandler import LocationHandler
from web.handler.RoomsHandler import RoomsHandler
from web.handler.SensorHandler import SensorHandler
from web.handler.SensorsHandler import SensorsHandler
from web.handler.ConfigurationHandler import ConfigurationHandler
from web.handler.TokenAuthHandler import TokenAuthHandler
from web.handler.VoiceCommandHandler import VoiceCommandHandler

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
                TokenAuthHandler,
                dict(authentication=authentication, jwt_token_factory=container.jwt_token_factory()),
                name='api_token_login'
            ),
            url(r'/api/location', LocationHandler, name='api_location'),
            url(
                r'/api/voice-command',
                VoiceCommandHandler,
                dict(voice_commands=container.voice_commands()),
                name='api_voice_command'
            ),
            url(
                r'/api/rooms', RoomsHandler,
                dict(rooms_formatter=container.rooms_formatter()), name='api_rooms'
            ),
            url(
                r'/api/ifttt-list', IftttListHandler,
                dict(ifttt_formatter=container.ifttt_formatter()),
                name='api_ifttt_list'
            ),
            url(
                r'/api/ifttt', IftttHandler,
                dict(ifttt_rules_repository=container.ifttt_rules_repository(), rule_factory=container.rule_factory()),
                name='api_ifttt_add'
            ),
            url(
                r'/api/ifttt/(.*)', IftttHandler,
                dict(ifttt_rules_repository=container.ifttt_rules_repository(), rule_factory=container.rule_factory()),
                name='api_ifttt'
            ),
            url(
                r'/api/actuator/(.*)', ActuatorHandler,
                dict(async_actuator_commands=async_actuator_commands),
                name='api_actuator'
            ),
            url(
                r'/api/actuators', ActuatorsHandler,
                dict(actuators_formatter=container.actuators_formatter(), actuators_repository=actuators_repo),
                name='api_actuators'
            ),
            url(
                r'/api/sensors', SensorsHandler,
                dict(sensors_formatter=container.sensors_formatter(), sensors_repository=sensors_repo),
                name='api_actuators'
            ),
            url(
                r'/api/sensor/(.*)', SensorHandler,
                dict(sensors_formatter=container.sensors_formatter()),
                name='api_sensor'
            ),
            url(
                r'/api/configuration', ConfigurationHandler,
                dict(configuration_formatter=container.configuration_formatter(),
                     configuration_factory=container.configuration_factory(),
                     configuration_repository=container.configuration_repository()),
                name='api_configuration'
            ),
            url(r'/(.*)', StaticFileHandler, {
                'path': general.web_server['static_path']
            }),
        ])

app = make_app()
app.listen(general.web_server['application_port'])
IOLoop.current().start()