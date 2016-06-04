import logging

from tornado.ioloop import IOLoop
from tornado.web import Application, url, StaticFileHandler

from tools.dataContainer import dataContainer
from tools.jobControl import jobControll
from tools.locationTracker import locationTracker
from web.actuatorsHandler import actuatorsHandler
from web.apiHandler import apiHandler
from web.graphsBuilderHandler import graphsBuilderHandler
from web.loginHandler import loginHandler
from web.timeRulesHandler import timeRulesHandler
import config

dataContainer = dataContainer(config.redisConfig)
locationTracker = locationTracker(config.redisConfig)
jobControll = jobControll(config.redisConfig)
logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s] (%(threadName)-10s) %(message)s')

def make_app():
    global config, dataContainer, jobControll

    settings = {
        "cookie_secret": "wellithinksecretisnice",
        "login_url": "/login",
    }

    return Application([
            url(
                r"/actuator/([a-zA-Z1-9]+)/(on|off)",
                actuatorsHandler,
                dict(dataContainer=dataContainer, jobControll=jobControll),
                name="actuator-states"
            ),
            url(r'/login', loginHandler, dict(credentials=config.credentials), name='login'),
            url(r'/public/(.*)', StaticFileHandler, {'path': config.staticPath}),
            url(r'/graphs', graphsBuilderHandler, dict(dataContainer=dataContainer), name='graphs'),
            url(r'/time-rules', timeRulesHandler, dict(dataContainer=dataContainer, logging=logging), name='timeRules'),
            url(
                r'/api/(.*)',
                apiHandler,
                dict(dataContainer=dataContainer, credentials=config.credentials, locationTracker=locationTracker, logging=logging),
                name='api'
            ),
        ], **settings)

app = make_app()
app.listen(8080)
IOLoop.current().start()
