from typeguard import typechecked

from logging import RootLogger
from tools.JobControl import JobControll

class CommandRunner:
    @typechecked()
    def __init__(self, job_controll: JobControll, logging: RootLogger):
        self.__job_controll = job_controll
        self.__logging = logging

    @typechecked()
    def execute(self, command: str) -> None:
        pass