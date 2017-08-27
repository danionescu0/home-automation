from tornado.web import  authenticated

from tools.Authentication import Authentication
from web.BaseHandler import BaseHandler


class LogoutHandler(BaseHandler):
    @authenticated
    def get(self):
        self.clear_cookie(Authentication.AUTHENTICATION_COOKIE_NAME)
        self.redirect('/login')