import pprint

from container import Container
from datetime import datetime, timedelta

container = Container()

sensors_repo = container.sensors_repository()
sensors_formatter = container.sensors_formatter()

start_date = datetime.today() - timedelta(days=1)
end_date = datetime.today()

# pprint.pprint(sensors_repo.get_sensor_values('airPollution_living', start_date, end_date))
pprint.pprint(sensors_formatter.get_sensor_values('airPollution_living', start_date, end_date))
print("cici")