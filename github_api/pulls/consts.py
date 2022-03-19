from enum import Enum
from importlib import import_module


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
        module_name = f'.pulls.visualization.{self.value}_plot'
        return import_module(module_name, package='github_api')
