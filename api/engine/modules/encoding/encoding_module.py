import abc
from copy import deepcopy

from engine.models.record import *
from engine.modules.module import Module
from engine.utils.dynamic_loading import load_module


class EncodingModule(Module):
    """
    *IMPORTANT: All encoding modules must include a hidden input 'name' with value equal to the directory.
    This is because of dynamic loading inside of indexing modules (or potentially others modules).
    """
    def __init__(self, **kwargs):
        super(EncodingModule, self).__init__(**kwargs)

    @abc.abstractmethod
    def run(self, value):
        pass
