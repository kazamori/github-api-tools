from enum import Enum
from importlib import import_module

PACKAGE_NAME = 'github-api-tools'


class Plot(Enum):
    BOX = 'box'
    SCATTER = 'scatter'
    VIOLIN = 'violin'

    @classmethod
    def from_str(cls, s):
        for _, plot in cls.__members__.items():
            if s == plot.value:
                return plot
        raise NotImplementedError(f'Unsupported plot: {s}')

    @property
    def module(self):
        module_name = f'.visualization.{self.value}_plot'
        return import_module(module_name, package='github_api')


class WeekEnd(Enum):
    SATURDAY = 6
    SUNDAY = 7


class GithubFile(Enum):
    ADD = 'additions'
    DEL = 'deletions'
    CHG = 'changes'


class GithubState(Enum):
    OPEN = 'open'
    CLOSED = 'closed'
    ALL = 'all'
