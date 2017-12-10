from typing import List

from typeguard import typechecked

from communication.actuator.strategies.BaseStrategy import BaseStrategy


class ActuatorStrategies():
    @typechecked()
    def __init__(self) -> None:
        self.__strategies = []

    def add_strategy(self, strategy: BaseStrategy) -> None:
        self.__strategies.append(strategy)

    def get_strategies(self) -> List[BaseStrategy]:
        return self.__strategies