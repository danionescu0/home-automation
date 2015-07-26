from datetime import datetime
from tornado.ioloop import IOLoop
from tornado.web import RequestHandler, Application, url, authenticated, StaticFileHandler
import serial
import threading
import time
import logging

import homeAutomationBt
import homeAutomationCommParser
from brain import brain
from dataContainer import dataContainer

btSeparator = '|'
btBuffer1 = btBuffer2 = "";
courtainsMode = 'none'
courtainsTime = datetime.now()
credentials = {'username' : 'dan', 'password' : 'cicibici07'}
staticPath = '/home/pi/home-automation/python-server/public'

logging.basicConfig(level=logging.DEBUG,
                    format='[%(levelname)s] (%(threadName)-10s) %(message)s',
                    )
port = serial.Serial("/dev/ttyAMA0", baudrate=9600, timeout=3.0)
btComm = homeAutomationBt.connectAllBt()
logging.debug('Finished connectiong to BT devices')
dataContainer = dataContainer('127.0.0.1:11211')
homeBrain = brain(btComm, port, dataContainer)

class BaseHandler(RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("user")

class LoginHandler(BaseHandler):
    def get(self):
        self.render("html/login.html")

    def post(self):
        username = self.get_argument("username", default=None, strip=False)
        password = self.get_argument("password", default=None, strip=False)
        if (username == credentials['username'] and password == credentials['password']):
            self.set_secure_cookie("user", username)
            self.redirect("/actuator/test/on")
            return

        self.redirect("/login")

class CourtainHandler(BaseHandler):
    @authenticated
    def get(self, mode, date, time):
        global courtainsTime, courtainsMode;
        self.write("Timer set!")
        courtainsMode = mode
        courtainsTime = datetime.strptime(date + ' ' + time, '%Y-%m-%d %H:%M')
        print(courtainsTime)

class ActuatorsHandler(BaseHandler):
    global dataContainer
    @authenticated
    def get(self, actuator, state):
        actuators = dataContainer.getActuators()
        if actuator in actuators and state in ['on', 'off']:
            state = (False, True)[state == 'on']
            dataContainer.setActuator(actuator, state)
            homeBrain.changeActuator(actuator, state)

        actuators = dataContainer.getActuators()
        self.render("html/main.html", actuators = actuators, sensors = dataContainer.getSensors())

def make_app():
    settings = {
        "cookie_secret": "wellithinksecretisnice",
        "login_url": "/login",
    }

    return Application([
            url(r"/set-courtain/(on|off)/([0-9\-]+)/([0-9:]+)", CourtainHandler, name="courtains-setter"),
            url(r"/actuator/([a-zA-Z]+)/(on|off)", ActuatorsHandler, name="actuator-states"),
            url(r"/login", LoginHandler, name="login"),
            url(r'/public/(.*)', StaticFileHandler, {'path': staticPath}),
        ], **settings)

def httpListener():
    app = make_app()
    app.listen(8080)
    IOLoop.current().start()

def timerCourtainsCheck():
    global courtainsTime, courtainsMode
    while True:
        time.sleep(60)
        now = datetime.now()
        if courtainsMode == 'on' and now.month == courtainsTime.month and now.day == courtainsTime.day\
                and now.hour == courtainsTime.hour and now.minute == courtainsTime.minute:
            logging.debug("time reached")
            btComm['bedroom'].send("3")

def btSensorsPolling(btSeparator, btBuffer, dataContainer, btComm):
    while True:
        data = btComm.recv(10)
        btBuffer += data
        if btBuffer.endswith(btSeparator):
            btBuffer = btBuffer[:-1]
            logging.debug("senzors received : " + btBuffer)
            data = homeAutomationCommParser.parseSensorsString(btBuffer)
            for key, value in data.iteritems():
                dataContainer.setSensor(key, value)
                homeBrain.sensorsUpdate(key)
            logging.debug(dataContainer.getSensors())
            btBuffer = ''

# initiating all threads
thr0 = threading.Thread(name='httpListener', target=httpListener)
thr1 = threading.Thread(
    name='bedroomSenzorPooling',
    target=btSensorsPolling,
    args=(btSeparator, btBuffer1, dataContainer, btComm['bedroom'])
)
thr2 = threading.Thread(
    name='livingSenzorPooling',
    target=btSensorsPolling,
    args=(btSeparator, btBuffer2, dataContainer, btComm['sensors'])
)
thr4 = threading.Thread(name='timerCourtainsCheck', target=timerCourtainsCheck)
for thread in [thr0, thr1, thr2, thr4]:
    thread.start()

