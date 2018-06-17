## Weather prediction using machine learning (tensorflow) and local weather data from the weather station


This subproject is a work in prgress, and it will try to predict the rain on the next 6 hours perios using previous data from
the weather station.

The input data will previous information gathered locally from the weather station on the following sensors:

- temperature 

- humidity

- pressure

- light

- rain levels

The output data will be prediction on rain levels for the next 6 hours

Steps:

1. Use data_extractor.py weather_extraction.csv number_of_days to extract data from the home
automation project.

Open the file and replace ip with your own, also replace sensor names with your own names if necessary

2. training.py weather_extraction.csv

This will train the prediction model and create a tensor flow model

3. predict.py weather_extraction_test.csv

weather_extraction_test.csv file will contain data from which hasn't been trained on (future data) and will try to 
predict the weather for each line  