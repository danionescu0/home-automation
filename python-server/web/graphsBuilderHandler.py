import json
import logging
from tornado.web import  authenticated
from datetime import datetime, timedelta
from dateutil import tz
from web.baseHandler import baseHandler

class graphsBuilderHandler(baseHandler):
    def initialize(self, dataContainer):
        super(baseHandler, self).initialize()
        self.dataContainer = dataContainer

    @authenticated
    def get(self):
        data = self.__getDataFromDb('light', 1, None)
        self.render("../html/graphs.html",
                    datetimeList = json.dumps(data["datetimeList"]),
                    datapointValues = json.dumps(data["datapointValues"]),
                    selectedType = type,
                    menuSelected ="graphs",
                    selectedDaysBehind =  1,
                    selectedGroupedByHours =  0
                    )

    @authenticated
    def post(self, *args, **kwargs):
        logging.debug(self.get_argument('type', 'light'))
        type = self.get_argument('type', 'light')
        groupByHours = int(self.get_argument("group_by_hours", None, True))
        nrDaysBehind = int(self.get_argument("nr_days_behind", None, True))
        if groupByHours == 0:
            data = self.__getDataFromDb(type, nrDaysBehind, None)
        else:
            data = self.__getDataFromDb(type, nrDaysBehind, groupByHours)

        self.render("../html/graphs.html",
                    datetimeList = json.dumps(data["datetimeList"]),
                    datapointValues = json.dumps(data["datapointValues"]),
                    selectedType = type,
                    menuSelected ="graphs",
                    selectedDaysBehind =  nrDaysBehind,
                    selectedGroupedByHours =  groupByHours
                    )

    def __getDataFromDb(self, type, nrDaysBehind, groupByHours):
        startDate = datetime.today() - timedelta(days=nrDaysBehind)
        endDate = datetime.today()
        data = self.dataContainer.getSensorValuesInInterval(startDate, endDate, groupByHours)
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

        return {"datapointValues": datapointValues, "datetimeList" : datetimeList}