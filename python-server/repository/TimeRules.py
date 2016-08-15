import json
from datetime import datetime
from dateutil import tz

from repository.AbstractRedis import AbstractRedis

class TimeRules(AbstractRedis):
    __REDIS_KEY = 'time_rules'

    def __init__(self, configuration):
        AbstractRedis.__init__(self, configuration)
        self.keys = {'time_rules': {}}

    def upsert(self, name, actuator, state, time, active):
        rules = self.get(self.__REDIS_KEY)
        rules[name] = {
            'actuator' : actuator,
            'state' : state,
            'active': active,
            'time' : time.isoformat()
        }

        return self.client.set(self.__REDIS_KEY, json.dumps(rules))

    def delete(self, name):
        rules = self.get(self.__REDIS_KEY)
        rules.pop(name, None)

        return self.client.set(self.__REDIS_KEY, json.dumps(rules))

    def get_all(self):
        rules = self.get(self.__REDIS_KEY)
        if not rules:
            return {}
        for rule in rules:
            rules[rule]['stringTime'] = rules[rule]['time']
            rules[rule]['time'] = datetime.strptime(rules[rule]['time'], "%H:%M:%S").time()

        return rules

    def get_rules_that_match(self):
        from_zone = tz.gettz('UTC')
        to_zone = tz.gettz('Europe/Bucharest')

        rules = self.get_all()
        initial_date = datetime.now().replace(tzinfo=from_zone)
        local_date = initial_date.astimezone(to_zone)
        current_time = local_date.strftime('%H:%M:00')

        filtered = {}
        for key, rule_data in rules.iteritems():
            if rule_data['stringTime'] != current_time or rule_data['active'] != True:
                continue
            filtered[key] = rule_data

        return filtered