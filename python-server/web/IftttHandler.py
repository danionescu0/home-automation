import json

from typeguard import typechecked

from web.CorsHandler import CorsHandler
from web.security.secure import secure
from web.factory.RuleFactory import RuleFactory
from repository.IftttRulesRepository import IftttRulesRepository


class IftttHandler(CorsHandler):
    @typechecked()
    def initialize(self, ifttt_rules_repository: IftttRulesRepository, rule_factory: RuleFactory):
        self.__ifttt_rules_repository = ifttt_rules_repository
        self.__rule_factory = rule_factory

    @secure
    def post(self, id):
        request_data = json.loads(self.request.body.decode("utf-8"))
        rule = self.__rule_factory.from_request_data(request_data)
        self.__ifttt_rules_repository.upsert(rule)
        self.set_status(200)

    @secure
    def put(self):
        request_data = json.loads(self.request.body.decode("utf-8"))
        rule = self.__rule_factory.from_request_data(request_data)
        self.__ifttt_rules_repository.upsert(rule)
        self.set_status(200)

    @secure
    def delete(self, id):
        self.__ifttt_rules_repository.delete(id)
        self.set_status(200)