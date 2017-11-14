class ActuatorProperties:
    COMMUNICATOR = 'communicator'
    SEND_TO_DEVICE = 'send_to_device'
    COMMAND = 'command'
    ENCRIPTION = 'encription'

    def __init__(self) -> None:
        self.__properties = {}

    def set(self, name: str, value):
        self.__properties[name] = value

    def get(self, name: str):
        if name not in self.__properties:
            return None

        return self.__properties[name]

    def __repr__(self) -> str:
        description = "ActuatorProperties:"
        for key, value in self.__properties.items():
            description += '{0}: ({2}), '.format(key, value)

        return description