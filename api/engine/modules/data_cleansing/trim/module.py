# coding=utf-8
from engine.models.record import *
from engine.modules.data_cleansing.data_cleansing_module import DataCleansingModule
from engine.modules.extraction.extraction_module import ExtractionModule
from engine.modules.module import Module


class TrimWhitespaces(DataCleansingModule):
    """
        Pasa todos los valores de los fields de la columna a lower case
    """

    def __init__(self, **kwargs):
        super(TrimWhitespaces, self).__init__(**kwargs)

    @staticmethod
    def pretty_name():
        return "Trim whitespaces"

    def run(self, column):
        for field in column.fields:
            if field.tipe.value == EnumType.string.value:
                field.value = field.value.strip()

        return column
