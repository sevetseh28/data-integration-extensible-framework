import abc
from copy import deepcopy
from decimal import *
from engine.models.record import *
from engine.modules.module import Module
from datetime import datetime
from copy import deepcopy
from unidecode import unidecode

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

    def get_field_from_value(self, value):
        """
        this method receives a raw extracted value by a specific Extraction module and returns a Field object
        with the corrrect type
        :return: Field object
        """
        if isinstance(value, str):
            return Field(value, EnumType.string)
        elif isinstance(value, unicode):
            return Field(unidecode(value), EnumType.string)
        elif isinstance(value, int) or isinstance(value, long) or isinstance(value, float) or type(
                value).__name__ == 'Int64':
            return Field(value, EnumType.number)
        elif isinstance(value, bool):
            return Field(value, EnumType.boolean)
        elif isinstance(value, datetime):
            return Field(value, EnumType.date)
        elif type(value) is type(None):
            return Field(value, EnumType.null)
        elif type(value) is Decimal:
            return Field(str(value), EnumType.number)
        else:
            return Field(str(value), EnumType.string)

    @abc.abstractmethod
    def run(self):
        raise NotImplementedError

