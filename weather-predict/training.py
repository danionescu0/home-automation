import sys
import pandas as pd
from sklearn.model_selection import train_test_split
import numpy

from ModelPreparator import ModelPreparator
from learning import get_dnn_regressor, wx_input_fn


file_name = sys.argv[1]
number_iterations = int(sys.argv[2])

model_preparator = ModelPreparator()
dataframe = model_preparator.prepare(pd.read_csv(file_name))

input_data = dataframe[[col for col in dataframe.columns if col != 'has_rain']]
output_data = dataframe['has_rain']

input_train, input_tmp, output_train, output_tmp = \
        train_test_split(
            input_data,
            output_data,
            test_size=0.2,
            random_state=23
        )
regressor = get_dnn_regressor(input_data)

evaluations = []
STEPS = 400
for i in range(number_iterations):
    regressor.train(input_fn=wx_input_fn(input_train, y=output_train), steps=STEPS)
    print(regressor.evaluate(
        input_fn=wx_input_fn(input_train, output_train, num_epochs=1, shuffle=False))
    )
