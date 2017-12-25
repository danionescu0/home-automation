from typeguard import typechecked

from repository.ConfigurationRepository import ConfigurationRepository


class ConfigurationFormatter:
    @typechecked()
    def __init__(self, configuration_repository: ConfigurationRepository) -> None:
        self.__configuration_repository = configuration_repository

    @typechecked()
    def get_all(self) -> list:
        configs = self.__configuration_repository.get_all()
        formatted = []
        for config in configs.items():
            attributes = vars(config[1])
            attributes.update({
                'name' : config[0],
                'main_description' : config[1].main_description(),
                'properties_description' : config[1].properties_description()
            })
            formatted.append(attributes)

        return formatted
