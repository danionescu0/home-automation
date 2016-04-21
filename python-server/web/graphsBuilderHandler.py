import json
import logging
from tornado.web import Application, url, authenticated, StaticFileHandler
from datetime import datetime, timedelta
from dateutil import tz
from web.baseHandler import baseHandler

class graphsBuilderHandler(baseHandler):
    def initialize(self, dataContainer):
        self.dataContainer = dataContainer

    @authenticated
    def get(self):
        self.__displayPage('light')

    @authenticated
    def post(self, *args, **kwargs):
        logging.debug(self.get_argument('type', 'light'))
        type = self.get_argument('type', 'light')
        self.__displayPage(type)

    def __displayPage(self, type):
        startDate = datetime.today() - timedelta(days=1)
        endDate = datetime.today()
        data = self.dataContainer.getSensorValuesInInterval(startDate, endDate)
        datetimeList = []
        datapointValues = []
        from_zone = tz.gettz('UTC')
        to_zone = tz.gettz('Europe/Bucharest')
        lastValueBySenzorType = {}
        for datapoint in data:
            initialDate = datetime.fromtimestamp(int(datapoint['timestamp'])).replace(tzinfo=from_zone)
            bucharestDate = initialDate.astimezone(to_zone)
            datetimeAsString = bucharestDate.strftime('%Y-%m-%d %H:%M:%S')
            datetimeList.append(datetimeAsString)
            if type in datapoint.keys():
                datapointValues.append(datapoint[type])
                lastValueBySenzorType[type] = datapoint[type]
            elif type in lastValueBySenzorType.keys():
                datapointValues.append(lastValueBySenzorType[type])
            else:
                datapointValues.append(0)

        self.render("../html/graphs.html",
                    datetimeList = json.dumps(datetimeList),
                    datapointValues = json.dumps(datapointValues),
                    selectedType = type,
                    menuSelected="graphs"
                    )