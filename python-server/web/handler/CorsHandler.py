import tornado


class CorsHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with, content-type, authorization")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, PUT, DELETE')

    def options(self, *args, **kwargs):
        self.set_status(204)
        self.finish()