from model.DataSource import DataSource
from model.SensorTypes import SensorTypes


class SensorTypeDatasourceMap:
    MAP = {
        DataSource.WEATHER_STATION.value: [
            SensorTypes.TEMPERATURE.value, SensorTypes.HUMIDITY.value, SensorTypes.PRESSURE.value,
            SensorTypes.RAIN.value, SensorTypes.LIGHT.value
        ],
        DataSource.DARKSKY.value: [
            SensorTypes.TEMPERATURE.value, SensorTypes.HUMIDITY.value, SensorTypes.PRESSURE.value,
            SensorTypes.RAIN.value, SensorTypes.WIND_SPEED.value, SensorTypes.WIND_SPEED.value,
            SensorTypes.UV_INDEX.value, SensorTypes.VISIBILITY.value
        ],
    }

    def get(self, datasource: str) -> list:
        if datasource not in self.MAP:
            raise Exception('Mapping for datasoruce {0} not found'.format(datasource))

        return self.MAP[datasource]