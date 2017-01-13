import abc
from copy import deepcopy

from engine.models.record import *
from engine.modules.module import Module
from engine.utils.dynamic_loading import load_module


class ExportModule(Module):
    def __init__(self, **kwargs):
        super(ExportModule, self).__init__(**kwargs)

    @abc.abstractmethod
    def run(self):
        raise NotImplementedError

