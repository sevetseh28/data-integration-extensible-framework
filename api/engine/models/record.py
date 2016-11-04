import collections
from json import JSONEncoder

from enum import Enum


class Record:
    def __init__(self):
        # columns es un diccionario con columnas como claves y listas de fields como valores
        self.columns = {}

    def to_json(self):
        return {
            c.to_string(): [f.to_json() for f in self.columns[c]]
            for c in self.columns
            }


class Column:
    def __init__(self, name):
        self.name = name

    @staticmethod
    def from_json(json):
        return Column(json["name"])

    def to_json(self):
        return self.__dict__

    def to_string(self):
        return self.name


class Field:
    def __init__(self, value, tipe, tags=None, output_field=None, column=None):
        if tags is None:
            tags = []

        self.value = value
        self.tipe = tipe
        self.tags = tags
        self.output_field = output_field
        self.column = column

    def to_json(self):
        json = self.__dict__
        json["column"] = self.column.to_json()
        json["tipe"] = self.tipe.to_json()

        return json


"""
Representa la coleccion de columnas matcheadas.
Es una lista de pares de conjuntos de columnas donde los elementos del par son las columnas que matchean con las otras.
[
    {
        "source1": [col11, col12, ..],
        "source2": [col21, col22, ..]
    },
    {
        "source1": [col14, col15, ..],
        "source2": [col24, col25, ..]
    },
    ...
]
"""


class SchemaMatch:
    def __init__(self):
        self.schema_matches = []

    def add_match(self, columns_source1, columns_source2):
        self.schema_matches.append({
            "source1": columns_source1,
            "source2": columns_source2,
        })

    def to_json(self):
        return [{
                    "source1": [c.to_json() for c in match['source1']],
                    "source2": [c.to_json() for c in match['source2']]
                } for match in self.schema_matches]


class FieldType(Enum):
    string = 1
    number = 2
    date = 3
    boolean = 4

    def to_json(self):
        return self.value
