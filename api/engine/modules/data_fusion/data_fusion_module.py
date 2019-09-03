import abc

from engine.modules.module import Module


class DataFusionModule(Module):
    def __init__(self, **kwargs):
        super(DataFusionModule, self).__init__(**kwargs)

    @abc.abstractmethod
    def run(self):
        raise NotImplementedError
