# coding=utf-8
from engine.models.record import *
from engine.modules.extraction.extraction_module import ExtractionModule
from engine.modules.module import Module


class DeleteChars(Module):
    """
        Elimina caracteres no deseados de los fields de la columna

        Config:
        {
            "chars":[string con chars a eliminar concatenados, p.ej: ".-!"
        }
    """

    def __init__(self, **kwargs):
        super(DeleteChars, self).__init__(**kwargs)

    @staticmethod
    def pretty_name():
        return "Delete chars"

    def run(self, column):
        for field in column.fields:
            if field.tipe.value == FieldType.string.value:
                field.value = field.value.__str__().translate(None, self.config["chars"])

        return column

    @staticmethod
    def config_json(**kwargs):
        return {
            'chars': {
                'label': 'Characters',
                'type': 'text'
            }
        }
