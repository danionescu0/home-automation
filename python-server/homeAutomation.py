from tornado.ioloop import IOLoop
from tornado.web import RequestHandler, Application, url, authenticated, StaticFileHandler
import serial
import threading
import logging

import homeAutomationCommParser
from brain import brain
from dataContainer import dataContainer
from homeAutomationBt import btConnections

btSeparator = '|'
btBuffer1 = btBuffer2 = "";
credentials = {'username' : 'dan', 'password' : 'cicibici07'}
staticPath = '/home/pi/home-automation/python-server/public'
btConns = {'bedroom' : '00:14:01:13:16:44', 'living' : '20:14:12:08:20:45'}

logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s] (%(threadName)-10s) %(message)s')
serialPort = serial.Serial("/dev/ttyAMA0", baudrate=9600, timeout=3.0)
btComm = btConnections(btConns['bedroom'], btConns['living']).connectAllBt()
logging.debug('Finished connectiong to BT devices')
dataContainer = dataContainer('127.0.0.1:11211')
homeBrain = brain(btComm, serialPort, dataContainer)

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
            url(r"/actuator/([a-zA-Z]+)/(on|off)", ActuatorsHandler, name="actuator-states"),
            url(r"/login", LoginHandler, name="login"),
            url(r'/public/(.*)', StaticFileHandler, {'path': staticPath}),
        ], **settings)

def httpListener():
    app = make_app()
    app.listen(8080)
    IOLoop.current().start()

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
    args=(btSeparator, btBuffer2, dataContainer, btComm['living'])
)
for thread in [thr0, thr1, thr2]:
    thread.start()

