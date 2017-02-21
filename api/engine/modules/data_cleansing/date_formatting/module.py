# coding=utf-8
from unidecode import unidecode

from engine.models.record import *
from engine.modules.data_cleansing.data_cleansing_module import DataCleansingModule
from engine.modules.module import Module
import dateparser


class DateFormatting(DataCleansingModule):
    """
        Formatea como date los valores que logra parsear, los que no, quedán como estaban.

        Config:
        {
        languages:['en','es']
        }
    """

    def __init__(self, **kwargs):
        super(DateFormatting, self).__init__(**kwargs)

    @staticmethod
    def pretty_name():
        return "Date Formatting"

    def run(self, column):
        languages = self.config["languages"]
        for field in column.fields:
            if field.tipe.value == EnumType.string.value:
                parsed = dateparser.parse(field.value,languages=languages)
                if parsed is not None:
                    field.value = parsed
                    field.tipe = EnumType.date

        return column

    @staticmethod
    def config_json(**kwargs):
        return {
            "languages": {
                "label": "Languages",
                "type": "multipleselect",
                "options": [
                    "es",
                    "en",
                    "pt",
                    "fr",
                    "ru"
                ]
            }
        }
