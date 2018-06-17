import sys
import pandas as pd

import tensorflow as tf
from sklearn.model_selection import train_test_split
from ModelPreparator import ModelPreparator


file_name = sys.argv[1]
model_preparator = ModelPreparator()
dataframe = model_preparator.prepare(pd.read_csv(file_name))

input = dataframe[[col for col in dataframe.columns if col != 'rain_outside_max']]
output = dataframe['rain_outside_max']
input_train, input_tmp, output_train, output_tmp = train_test_split(input, output, test_size=0.2, random_state=23)
feature_cols = [tf.feature_column.numeric_column(col) for col in input.columns]

regressor = tf.estimator.DNNRegressor(feature_columns=feature_cols,
                                      hidden_units=[50, 50],
                                      model_dir='tf_rain_model')

def wx_input_fn(X, y=None, num_epochs=None, shuffle=True, batch_size=400):
    return tf.estimator.inputs.pandas_input_fn(x=X,
                                               y=y,
                                               num_epochs=num_epochs,
                                               shuffle=shuffle,
                                               batch_size=batch_size)

evaluations = []
STEPS = 400
for i in range(100):
    regressor.train(input_fn=wx_input_fn(input_train, y=output_train), steps=STEPS)
    print(regressor.evaluate(
        input_fn=wx_input_fn(input_train, output_train, num_epochs=1, shuffle=False))
    )
