from tornado.web import RequestHandler
from listener.saveLocationListener import saveLocationListener

class baseHandler(RequestHandler):
    def initialize(self):
        saveLocationListener()

    def render(self, template, **kwargs):
        kwargs['username'] = self.get_secure_cookie("user")
        super(baseHandler, self).render(template, **kwargs)

    def get_current_user(self):
        return self.get_secure_cookie("user")
