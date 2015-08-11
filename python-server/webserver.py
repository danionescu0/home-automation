import json
import logging
from tornado.ioloop import IOLoop
from tornado.web import RequestHandler, Application, url, authenticated, StaticFileHandler
import config
from dataContainer import dataContainer
from jobControl import jobControll
from datetime import datetime, timedelta
import time

dataContainer = dataContainer(config.redisConfig)
jobControll = jobControll(config.redisConfig)
logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s] (%(threadName)-10s) %(message)s')

class BaseHandler(RequestHandler):
    def render(self, template, **kwargs):
        kwargs['username'] = self.get_secure_cookie("user")
        super(BaseHandler, self).render(template, **kwargs)

    def get_current_user(self):
        return self.get_secure_cookie("user")

class LoginHandler(BaseHandler):
    def initialize(self, credentials):
        self.credentials = credentials

    def get(self):
        self.render("html/login.html")

    def post(self):
        username = self.get_argument("username", default=None, strip=False)
        password = self.get_argument("password", default=None, strip=False)
        if (username == self.credentials['username'] and password == self.credentials['password']):
            self.set_secure_cookie("user", username)
            self.redirect("/actuator/test/on")
            return

        self.redirect("/login")

class ActuatorsHandler(BaseHandler):
    def initialize(self, dataContainer, jobControll):
        self.dataContainer = dataContainer
        self.jobControll = jobControll

    @authenticated
    def get(self, actuator, state):
        actuators = self.dataContainer.getActuators()
        if actuator in actuators and state in ['on', 'off']:
            state = (False, True)[state == 'on']
            self.jobControll.addJob(json.dumps({"job_name": "actuators", "actuator": actuator, "state" : state}))
            time.sleep(0.3)
        actuators = self.dataContainer.getActuators()

        self.render("html/main.html", actuators = actuators, sensors = self.dataContainer.getSensors())

class GraphsBuilderHandler(BaseHandler):
    def initialize(self, dataContainer):
        self.dataContainer = dataContainer

    @authenticated
    def get(self):
        self.__displayPage('light')

    @authenticated
    def post(self, *args, **kwargs):
        logging.debug(self.get_argument('type', 'light'))
        type = self.get_argument('type', 'light')
        self.__displayPage(type)

    def __displayPage(self, type):
        startDate = datetime.today() - timedelta(days=1)
        endDate = datetime.today()
        data = self.dataContainer.getSensorValuesInInterval(startDate, endDate)
        datetimeList = []
        datapointValues = []
        for datapoint in data:
            datetimeAsString = datetime.fromtimestamp(int(datapoint['timestamp'])).strftime('%Y-%m-%d %H:%M:%S')
            datetimeList.append(datetimeAsString)
            if type in datapoint.keys():
                datapointValues.append(datapoint[type])
            else:
                datapointValues.append(0)

        self.render("html/graphs.html",
                    datetimeList = json.dumps(datetimeList),
                    datapointValues = json.dumps(datapointValues),
                    selectedType = type
                    )
class TimeRulesHandler(BaseHandler):
    def initialize(self, dataContainer):
        self.dataContainer = dataContainer

    @authenticated
    def get(self):
        self.render("html/timeRules.html",
                    rules = self.dataContainer.getTimeRules()
                    )


def make_app():
    global config, dataContainer, jobControll

    settings = {
        "cookie_secret": "wellithinksecretisnice",
        "login_url": "/login",
    }

    return Application([
            url(
                r"/actuator/([a-zA-Z]+)/(on|off)",
                ActuatorsHandler,
                dict(dataContainer=dataContainer, jobControll=jobControll),
                name="actuator-states"
            ),
            url(r"/login", LoginHandler, dict(credentials=config.credentials), name="login"),
            url(r'/public/(.*)', StaticFileHandler, {'path': config.staticPath}),
            url(r'/graphs', GraphsBuilderHandler, dict(dataContainer=dataContainer), name="graphs"),
            url(r'/time-rules', TimeRulesHandler, dict(dataContainer=dataContainer), name="timeRules"),
        ], **settings)

app = make_app()
app.listen(8080)
IOLoop.current().start()
