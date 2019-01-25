import argparse
from datetime import datetime, timedelta

import pandas
import matplotlib.pyplot as plt

from container import Container
from model.DataSource import DataSource


argparse = argparse.ArgumentParser()
argparse.add_argument("-d", "--days-behind", required=True, dest="days_behind", type=int,
                      help="Days behind to be taken into account")
args = vars(argparse.parse_args())

container = Container()
datapoints_repository = container.datapoints_repository()
start_date = datetime.today() - timedelta(days=args['days_behind'])
end_date = datetime.today()
extracted_data = datapoints_repository.get(DataSource.WEATHER_STATION.value, start_date, end_date)
dataframe = pandas.DataFrame(extracted_data).set_index('_id')


fig, axes = plt.subplots(5, figsize=(13, 8))
dataframe.plot(subplots=True, kind='line', x='date', y='temperature', ax=axes[0])
dataframe.plot(subplots=True, kind='line', x='date', y='pressure', color='red', ax=axes[1])
dataframe.plot(subplots=True, kind='line', x='date', y='humidity', color='blue', ax=axes[2])
dataframe.plot(subplots=True, kind='line', x='date', y='light', color='purple', ax=axes[3])
dataframe.plot(subplots=True, kind='line', x='date', y='rain', color='black', ax=axes[4])

plt.show()