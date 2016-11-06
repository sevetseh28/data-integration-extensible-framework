import collections
from json import JSONEncoder

from enum import Enum


class Record:
    def __init__(self, columns=None):
        # columns es un diccionario <string, column> donde el string es el nombre de la columna
        if columns is None:
            columns = {}

        self.columns = columns

    def to_json(self):
        return {
            n: c.to_json()
            for n, c in self.columns.items()
            }

    @staticmethod
    def from_json(json):
        return Record({n: Column.from_json(c) for n, c in json.items()})


class Column:
    def __init__(self, name, fields=None):
        if fields is None:
            fields = []

        self.name = name
        self.fields = fields

    @staticmethod
    def from_json(json):
        return Column(json["name"], [Field.from_json(f) for f in json["fields"]])

    def to_json(self, with_fields=True):
        json = {
            "name": self.name,
        }

        if with_fields:
            json["fields"] = [f.to_json() for f in self.fields]

        return json

    def concat_fields(self):
        result = ""
        for field in self.fields:
            result += str(field.value)

        return result


class Field:
    def __init__(self, value, tipe, tags=None, output_field=None):
        if tags is None:
            tags = []

        self.value = value
        self.tipe = tipe
        self.tags = tags
        self.output_field = output_field

    def to_json(self):
        json = dict(self.__dict__)
        json["tipe"] = self.tipe.to_json()

        return json

    @staticmethod
    def from_json(json):
        return Field(json["value"], FieldType.from_json(json["tipe"]), json["tags"], json["output_field"])


class SchemaMatch:
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

    def __init__(self):
        self.schema_matches = []

    def add_match(self, columns_source1, columns_source2):
        self.schema_matches.append({
            "source1": columns_source1,
            "source2": columns_source2,
        })

    def to_json(self):
        return [{
                    "source1": [c.to_json(with_fields=False) for c in match['source1']],
                    "source2": [c.to_json(with_fields=False) for c in match['source2']]
                } for match in self.schema_matches]


class IndexingGroup:
    def __init__(self, key, record_list1, record_list2):
        self.key = key
        self.records1 = record_list1
        self.records2 = record_list2

    def to_json(self):
        return [dict(r.to_json(), source=1, key=self.key) for r in self.records1] + \
               [dict(r.to_json(), source=2, key=self.key) for r in self.records2]


class FieldType(Enum):
    string = 1
    number = 2
    date = 3
    boolean = 4

    def to_json(self):
        return self.value

    @staticmethod
    def from_json(json):
        return FieldType(json)
