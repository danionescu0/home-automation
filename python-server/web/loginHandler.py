from web.baseHandler import baseHandler

class loginHandler(baseHandler):
    def initialize(self, credentials):
        super(baseHandler, self).initialize()
        self.credentials = credentials

    def get(self):
        self.render("../html/login.html", menuSelected="login")

    def post(self):
        username = self.get_argument("username", default=None, strip=False)
        password = self.get_argument("password", default=None, strip=False)
        if (username == self.credentials['username'] and password == self.credentials['password']):
            self.set_secure_cookie("user", username)
            self.redirect("/actuator/test/on")
            return

        self.redirect("/login")