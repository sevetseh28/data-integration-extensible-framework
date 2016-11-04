import collections
from json import JSONEncoder

from enum import Enum


class Record():
    def __init__(self):
        # columns es un diccionario con columnas como claves y listas de fields como valores
        self.columns = {}

    def to_json(self):
        return {c.to_json(): [f.to_json() for f in self.columns[c]] for c in self.columns}


class Column:
    def __init__(self, name):
        self.name = name

    def to_json(self):
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


class FieldType(Enum):
    string = 1
    number = 2
    date = 3
    boolean = 4

    def to_json(self):
        return self.value
