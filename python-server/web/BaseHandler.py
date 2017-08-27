from tornado.web import RequestHandler


class BaseHandler(RequestHandler):
    def render(self, template, **kwargs):
        kwargs['username'] = self.get_secure_cookie("user")
        super(BaseHandler, self).render(template, **kwargs)

    def get_current_user(self):
        return self.get_secure_cookie("user")