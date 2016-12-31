# coding=utf-8
from unidecode import unidecode

from engine.models.record import *
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
        chars = unidecode(self.config["chars"])
        for field in column.fields:
            if field.tipe.value == FieldType.string.value:
                field.value = field.value.__str__().translate(None, chars)

        return column

    @staticmethod
    def config_json(**kwargs):
        return {
            'chars': {
                'label': 'Characters to delete',
                'type': 'text'
            }
        }
