import abc
from copy import deepcopy

from engine.models.record import *
from engine.modules.module import Module
from engine.utils.dynamic_loading import load_module


class IndexingModule(Module):
    def __init__(self, **kwargs):
        super(IndexingModule, self).__init__(**kwargs)

        # si no hay config de encoding, crea una por defecto
       # if 'encoding' not in self.config or not self.config['encoding']:
      #      self.config['encoding'] = {
       #         'name': 'nop'
       #     }

        self.schema = []
        self.records = []
        #self.encoding_module = load_module("encoding", self.config['encoding']['name'],
                                 #          config=self.config['encoding'])

    @staticmethod
    def pretty_name():
        return "Indexing module"

    @abc.abstractmethod
    def run(self):
        pass

  #  def encode(self, value):
     #p   return self.encoding_module.run(value)
