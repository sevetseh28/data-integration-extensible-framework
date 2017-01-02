import abc
from copy import deepcopy

from engine.models.record import *
from engine.modules.module import Module


class ExtractionModule(Module):
    def __init__(self, **kwargs):
        super(ExtractionModule, self).__init__(**kwargs)
        self.schema = []
        self.records = []

    def add_to_schema(self, column):
        """
        appendea la columna al esquema si no existe ya otra con el mismo nombre
        """
        if len([c for c in self.schema if c.name == column.name]) > 0:
            return

        self.schema.append(deepcopy(column))

    @staticmethod
    def pretty_name():
        return "Extraction module"

    @abc.abstractmethod
    def run(self):
        pass
