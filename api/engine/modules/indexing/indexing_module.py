from copy import deepcopy

from engine.models.record import *
from engine.modules.module import Module
from engine.utils.dynamic_loading import load_module


class IndexingModule(Module):
    def __init__(self, encoding="nop", encoding_config=None, **kwargs):
        super(IndexingModule, self).__init__(**kwargs)
        self.schema = []
        self.records = []
        self.encoding_module = load_module("encoding", encoding, config=encoding_config)

    def encode(self, value):
        return self.encoding_module.run(value)
