import abc
from copy import deepcopy

from engine.models.record import *
from engine.modules.module import Module
from engine.utils.dynamic_loading import load_module


class ClassificationModule(Module):
    def __init__(self, **kwargs):
        super(ClassificationModule, self).__init__(**kwargs)

    @abc.abstractmethod
    def run(self, simil):
        pass
