import logging
from tornado.ioloop import IOLoop
from tornado.web import Application, url, authenticated, StaticFileHandler
import config
from dataContainer import dataContainer
from jobControl import jobControll
from web.timeRulesHandler import timeRulesHandler
from web.graphsBuilderHandler import graphsBuilderHandler
from web.loginHandler import loginHandler
from web.actuatorsHandler import actuatorsHandler

dataContainer = dataContainer(config.redisConfig)
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
            url(r"/login", loginHandler, dict(credentials=config.credentials), name="login"),
            url(r'/public/(.*)', StaticFileHandler, {'path': config.staticPath}),
            url(r'/graphs', graphsBuilderHandler, dict(dataContainer=dataContainer), name="graphs"),
            url(r'/time-rules', timeRulesHandler, dict(dataContainer=dataContainer, logging=logging), name="timeRules"),
        ], **settings)

app = make_app()
app.listen(8080)
IOLoop.current().start()
