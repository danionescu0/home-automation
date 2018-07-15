## Weather prediction using machine learning (keras with tensorflow) and local weather data from the weather station


The input data will previous information gathered locally from the weather station on the following sensors:

- temperature 

- humidity

- pressure

- light

- rain levels

The output data will be prediction on rain levels for the next 12 hours

Steps:

1. Generate the basic data using data_extractor.py

For example:

````
python prepare_model.py -i weather.csv -p 10 -d 10
````

2. Generate the model using prepare_model.py and show also the test values

````
python training.py -i weather_model.csv
````
