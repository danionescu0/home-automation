import sys
import argparse

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

from machine_learning.ModelBuilder import ModelBuilder
from machine_learning.GridSearch import GridSearch


argparse = argparse.ArgumentParser()
argparse.add_argument("-i", "--input-file", required=True, dest="input_file",
                      help="Input CSV file generated by data_extractor")
args = vars(argparse.parse_args())

model_builder = ModelBuilder()
grid_search = GridSearch(model_builder)


def read_from_csv(path: str) -> tuple:
    dataset = pd.read_csv(path).dropna()
    X = dataset.iloc[:, 3:].values
    y = dataset.iloc[:, 2].values
    return X, y

X, y = read_from_csv(args['input_file'])
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 0)
sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)
# print(grid_search.search(X_train, y_train))
# sys.exit()

classifier = model_builder.build(X.shape[1], 'adam')
classifier.fit(X_train, y_train, batch_size=9, nb_epoch=50)

# to be moved in separate file
XX, yy = read_from_csv('/home/ionescu/projects/python/home-automation/weather-predict/weather6h_model_test.csv')
i = good = 0

for test_data in XX:
    y_pred = classifier.predict(sc.transform(np.array([test_data])))
    will_rain = (y_pred > 0.5)
    if (will_rain == True and yy[i] == 1) or (will_rain == False and yy[i] == 0):
        good += 1
    print("Index: {0}, Actual: {1}, Predicted  {2}". format(i, yy[i], will_rain))
    i += 1

print ('Total: {0}, Good: {1}, Percent accuracy: {2} ', i, good, good * 100 / i)