from web.BaseHandler import BaseHandler
from tools.Authentication import Authentication

class LoginHandler(BaseHandler):
    def initialize(self, authentication):
        self.__authentication = authentication

    def get(self):
        self.render("./template/login.html", selected_menu_item="login")

    def post(self):
        username = self.get_argument("username", default=None, strip=False)
        password = self.get_argument("password", default=None, strip=False)
        if (self.__authentication.verify_credentials(username, password)):
            self.set_secure_cookie(Authentication.AUTHENTICATION_COOKIE_NAME, username)
            self.redirect("/")
            return

        self.redirect("/login")