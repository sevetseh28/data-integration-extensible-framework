# coding=utf-8
from engine.models.record import *
from engine.modules.extraction.extraction_module import ExtractionModule
from engine.modules.module import Module


class LowerCase(Module):
    """
        Pasa todos los valores de los fields de la columna a lower case
    """

    def __init__(self, **kwargs):
        super(LowerCase, self).__init__(**kwargs)

    def run(self, column):
        for field in column.fields:
            if field.tipe.value == FieldType.string.value:
                field.value = field.value.lower()

        return column
