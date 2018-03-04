class BaseDeviceProperties:
    def __init__(self) -> None:
        self.__properties = {}

    def set(self, name: str, value):
        self.__properties[name] = value

    def get(self, name: str):
        if name not in self.__properties:
            return None

        return self.__properties[name]

    def get_all(self):
        return self.__properties

    def __repr__(self) -> str:
        description = "Properties:"
        for key, value in self.__properties.items():
            description += '{0}: ({1}), '.format(key, value)

        return description