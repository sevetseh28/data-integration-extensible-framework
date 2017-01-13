import abc
from copy import deepcopy

from engine.models.record import *
from engine.modules.module import Module
from engine.utils.dynamic_loading import load_module


class IndexingModule(Module):
    def __init__(self, **kwargs):
        super(IndexingModule, self).__init__(**kwargs)

    @staticmethod
    def pretty_name():
        return "Indexing module"

    @abc.abstractmethod
    def run(self):
        """
        Runs the indexing module.
        :return: must return a Dict containing the groups. See below.
         format of return dict
            ret = {
                group_key_1: List[Record]
                group_key_2: List[Record]
                group_key_3: List[Record]
                ...
                group_key_n: List[Records]
            }
        """
        raise NotImplementedError
