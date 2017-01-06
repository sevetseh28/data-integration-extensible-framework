import abc
from copy import deepcopy

from engine.models.record import *
from engine.modules.module import Module
from engine.utils.dynamic_loading import load_module


class SchemaMatchingModule(Module):
    def __init__(self, **kwargs):
        super(SchemaMatchingModule, self).__init__(**kwargs)
        self.schema = []

    @abc.abstractmethod
    def run(self):
        pass

    def add_to_schema(self, column):
        """
        appendea la columna al esquema si no existe ya otra con el mismo nombre
        """
        if len([c for c in self.schema if c.name == column.name]) > 0:
            return

        self.schema.append(deepcopy(column))
