import collections
from json import JSONEncoder

from enum import Enum


class Record:
    def __init__(self, columns=None, id=None):
        # columns es un diccionario <string, column> donde el string es el nombre de la columna
        if columns is None:
            columns = {}

        self.columns = columns
        self._id = id

    def to_json(self):
        json = {
            'columns': [c.to_json() for n, c in self.columns.items()]
        }

        if self._id:
            json['_id'] = self._id

        return json

    def prefix_cols(self, prefix):
        for col in self.columns.values():
            if not col.name.startswith("__new__"):
                self.columns.pop(col.name)
                new_name = prefix + "_" + col.name
                col.name = new_name
                self.columns[new_name] = col

    def add_columns(self, cols, prefix=''):
        for col in cols:
            self.add_column(col, prefix)

    def remove_cols(self, cols):
        remove_cols = [c.name for c in cols]
        for col in self.columns.keys():
            if col in remove_cols:
                self.columns.pop(col)

    def add_column(self, col, prefix=''):
        if prefix:
            key = "{}-{}".format(prefix, col.name)
            col.name = key
        else:
            key = col.name

        self.columns[key] = col

    def get_output_field_col(self, out_field, col):
        result = ""

        col = self.columns[col]
        for f in col.fields:
            if f.output_field == out_field:
                result += str(f.value)

        return result

    def get_sourcex_cols(self, source_number):
        return [c for c in self.columns.values() if c.name.startswith("s{}".format(source_number))]

    def get_new_cols(self):
            return [c for c in self.columns.values() if c.name.startswith("__new__")]

    def matched_cols(self):
        return [c for c in self.columns.keys() if c.startswith("__new__")]

    def join_cols(self, cols, new_name):
        col_names = [c.name for c in cols]

        new_column = Column(new_name)
        for colname, col in self.columns.items():
            if colname in col_names:
                new_column.fields += col.fields

        self.columns[new_name] = new_column

    def get_col_names(self):
        return [self.columns.keys()]

    def get_cols(self, cols):
        return [col for col in self.columns.values() if col.name in cols]

    @staticmethod
    def from_json(json):
        id = json.pop("_id") if "_id" in json else None
        if 'key' in json: json.pop('key')
        if 'source' in json: json.pop('source')

        columns = {c["name"]: Column.from_json(c) for c in json['columns']}

        return Record(columns, id)


class Column:
    def __init__(self, name, fields=None):
        if fields is None:
            fields = []

        self.name = name
        self.fields = fields

    @staticmethod
    def from_json(json):
        fields = []
        if "fields" in json:
            fields = [Field.from_json(f) for f in json["fields"]]

        return Column(json["name"], fields)

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
        json["type"] = self.tipe.to_json()
        json.pop("tipe")

        return json

    @staticmethod
    def from_json(json):
        return Field(json["value"], FieldType.from_json(json["type"]), json["tags"], json["output_field"])


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
            "col_name": "__new__" + "-".join([c.name for c in columns_source1]),
            "source1": columns_source1,
            "source2": columns_source2,
        })

    def to_json(self):
        return [{
                    "col_name": match["col_name"],
                    "source1": [c.to_json(with_fields=False) for c in match['source1']],
                    "source2": [c.to_json(with_fields=False) for c in match['source2']]
                } for match in self.schema_matches]

    @staticmethod
    def from_json(json):
        matches = SchemaMatch()

        for match in json:
            cols1 = [Column.from_json(c) for c in match['source1']]
            cols2 = [Column.from_json(c) for c in match['source2']]

            matches.add_match(cols1, cols2)

        return matches


class IndexingGroup:
    def __init__(self, key, record_list1, record_list2):
        self.key = key
        self.records1 = record_list1
        self.records2 = record_list2

    def to_json(self):
        return [dict(r.to_json(), source=1, key=self.key) for r in self.records1] + \
               [dict(r.to_json(), source=2, key=self.key) for r in self.records2]


class SimilarityVector:
    def __init__(self, r1_id, r2_id, vector=None):
        if vector is None:
            vector = []

        self.record1 = r1_id
        self.record2 = r2_id

        self.vector = vector

    def to_json(self):
        return self.__dict__

    @staticmethod
    def from_json(json):
        return SimilarityVector(json['record1'], json['record2'], json['vector'])


class MatchResultType(Enum):
    no_match = 0
    match = 1
    undetermined = 2

    def to_json(self):
        return self.value

    @staticmethod
    def from_json(json):
        return FieldType(json)


class MatchResult:
    def __init__(self, r1_id, r2_id, likelihood=None, match_type=MatchResultType.no_match, id=None):
        self.record1 = r1_id
        self.record2 = r2_id

        self.match_type = match_type

        self.likelihood = likelihood
        self._id = id

    def to_json(self):
        json = self.__dict__

        if not self._id:
            json.pop('_id')

        json['match_type'] = self.match_type.to_json()
        return json

    @staticmethod
    def from_json(json):
        return MatchResult(json['record1'], json['record2'], json["likelihood"],
                           MatchResultType.from_json(json['match_type']), id=json['_id'])


class FieldType(Enum):
    string = 1
    number = 2
    date = 3
    boolean = 4
    null = 5
    notexist = 6

    def to_json(self):
        return self.value

    @staticmethod
    def from_json(json):
        return FieldType(json)
