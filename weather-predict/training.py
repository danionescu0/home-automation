import sys

import pandas as pd

from data_extractor.ModelPreparator import ModelPreparator

file_name = sys.argv[1]
number_iterations = int(sys.argv[2])

model_preparator = ModelPreparator()
dataframe, input_data, output_data = model_preparator.prepare(pd.read_csv(file_name), 4)
dataframe.to_csv("weather12_3.csv")
