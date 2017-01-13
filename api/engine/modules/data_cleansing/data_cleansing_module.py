import abc
from copy import deepcopy

from engine.models.record import *
from engine.modules.module import Module
from engine.utils.dynamic_loading import load_module


class DataCleansingModule(Module):
    def __init__(self, **kwargs):
        super(DataCleansingModule, self).__init__(**kwargs)

    @abc.abstractmethod
    def run(self, column):
        """

        :param column: a Column object
        :return: a Column object cleansed
        """
        raise NotImplementedError

