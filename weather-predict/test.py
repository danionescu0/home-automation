from datetime import datetime, timedelta

import pandas
import numpy


import config
from container import Container


extracted_data = []
days_behind = 1000
container = Container()

datapoints_repository = container.datapoints_repository()

for day_behind in range(days_behind, 0, -5):
    start_date = datetime.today() - timedelta(days=day_behind)
    end_date = datetime.today() - timedelta(days=(day_behind - 5))
    datapoints = datapoints_repository.get(start_date, end_date)
    extracted_data += datapoints

dataframe = pandas.DataFrame(extracted_data).set_index('_id')

total = good = rainy = 0
for index, row in dataframe.iterrows():
    total += 1
    if row['rain'] > 0:
        rainy += 1
    if row['rain'] > 0 and row['rain_prob'] > 0:
        good += 1
    print(row['date'], row['rain_prob'], row['rain'])

print('Total: {0}, Rain: {1}, Good: {2}'.format(total, rainy, good))

