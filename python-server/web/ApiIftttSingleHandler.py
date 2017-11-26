import json

from typeguard import typechecked

from web.CorsHandler import CorsHandler
from web.security.secure import secure
from repository.IftttRulesRepository import IftttRulesRepository


class ApiIftttSingleHandler(CorsHandler):
    @typechecked()
    def initialize(self, ifttt_rules_repository: IftttRulesRepository):
        self.__ifttt_rules_repository = ifttt_rules_repository

    @secure
    def post(self, id):
        data = json.loads(self.request.body.decode("utf-8"))
        print(data, id)
        self.set_status(200)