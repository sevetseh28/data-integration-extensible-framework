import abc

from engine.modules.module import Module


class ClassificationModule(Module):
    def __init__(self, **kwargs):
        super(ClassificationModule, self).__init__(**kwargs)

    @abc.abstractmethod
    def run(self, simil):
        raise NotImplementedError
