import abc
from copy import deepcopy

from engine.models.record import *
from engine.modules.module import Module
from engine.utils.dynamic_loading import load_module


class StandardisationTaggingModule(Module):
    def __init__(self, **kwargs):
        super(StandardisationTaggingModule, self).__init__(**kwargs)

    @abc.abstractmethod
    def run(self, column):
        """

        :param column:
        :return: a Column object
        """
        raise NotImplementedError
