from datetime import datetime
from tornado.ioloop import IOLoop
from tornado.web import RequestHandler, Application, url, authenticated, StaticFileHandler
import serial
import threading
import time
import logging

import homeAutomationBt
import homeAutomationCommParser

btSeparator = '|'
bt1SensorMessage = ''
bt2SensorMessage = ''
courtainsMode = 'none'
courtainsTime = datetime.now()
actuators = {'door' : False, 'window' :False, 'livingLight' : False, 'bedroomLight' : False}
credentials = {'username' : 'dan', 'password' : 'cicibici07'}
sensorsData = {'humidity' : 0, 'temperature' : 0, 'light' : 0}
staticPath = '/home/pi/home-automation/python-server/public'

logging.basicConfig(level=logging.DEBUG,
                    format='[%(levelname)s] (%(threadName)-10s) %(message)s',
                    )
port = serial.Serial("/dev/ttyAMA0", baudrate=9600, timeout=3.0)

btComm = homeAutomationBt.connectAllBt()
logging.debug('Finished connectiong to BT devices')

# refreshes bluetooth connection each 4 seconds  (sends something)
def btRefresher():
    while True:
        time.sleep(4)
        btComm['bedroom'].send("D")

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
    @authenticated
    def get(self, actuator, state):
        global btComm
        if actuator in actuators and state in ['on', 'off']:
            actuators[actuator] = (False, True)[state == 'on']
        if actuator == 'door':
            port.write("3")
        if actuator == 'livingLight':
            port.write("1")
        if actuator == 'bedroomLight':
            port.write("2")
        if actuator == 'window':
            if state == 'on':
               btComm['bedroom'].send("1")
            else:
               btComm['bedroom'].send("0")

        self.render("html/main.html", actuators = actuators, sensors = sensorsData)

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

def bt1SensorsPolling():
    global btSeparator, bt1SensorMessage, sensorsData
    while True:
        data = btComm['sensors'].recv(10)
        bt1SensorMessage += data
        if bt1SensorMessage.endswith(btSeparator):
            bt1SensorMessage = bt1SensorMessage[:-1]
            logging.debug("bt1 received : " + bt1SensorMessage)
            data = homeAutomationCommParser.parseSensorsString(bt1SensorMessage)
            for key, value in data.iteritems(): 
                sensorsData[key] = value
            logging.debug(sensorsData)
            bt1SensorMessage = ''


thr0 = threading.Thread(name='httpListener', target=httpListener)
thr1 = threading.Thread(name='btRefresher', target=btRefresher)
thr2 = threading.Thread(name='bt1SensorsPolling', target=bt1SensorsPolling)
thr4 = threading.Thread(name='timerCourtainsCheck', target=timerCourtainsCheck)
for thread in [thr0, thr1, thr2, thr4]:
# for thread in [thr0,  thr4]:
    thread.start()

