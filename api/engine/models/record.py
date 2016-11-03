from enum import Enum


class Record:
    def __init__(self):
        # columns es un diccionario con columnas como claves y listas de fields como valores
        self.columns = {}


class Column:
    def __init__(self, name):
        self.name = name


class Field:
    def __init__(self, value, tipe, tags=None, output_field=None, column=None):
        if tags is None:
            tags = []

        self.value = value
        self.tipe = tipe
        self.tags = tags
        self.output_field = output_field
        self.column = column


class FieldType(Enum):
    string = 1
    number = 2
    date = 3
    boolean = 4
