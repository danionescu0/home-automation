from web.BaseHandler import BaseHandler

class LoginHandler(BaseHandler):
    def initialize(self, credentials):
        self.credentials = credentials

    def get(self):
        self.render("../html/login.html", selected_menu_item="login")

    def post(self):
        username = self.get_argument("username", default=None, strip=False)
        password = self.get_argument("password", default=None, strip=False)
        if (username == self.credentials['username'] and password == self.credentials['password']):
            self.set_secure_cookie("user", username)
            self.redirect("/actuator/test/on")
            return

        self.redirect("/login")