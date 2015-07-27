import json
from tornado.ioloop import IOLoop
from tornado.web import RequestHandler, Application, url, authenticated, StaticFileHandler
import config
from dataContainer import dataContainer
from jobControl import jobControll

dataContainer = dataContainer(config.redisConfig)
jobControll = jobControll(config.redisConfig)

class BaseHandler(RequestHandler):
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
        actuators = self.dataContainer.getActuators()
        self.render("html/main.html", actuators = actuators, sensors = dataContainer.getSensors())

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
        ], **settings)

app = make_app()
app.listen(8080)
IOLoop.current().start()
