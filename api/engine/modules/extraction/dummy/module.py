# coding=utf-8
from engine.models.record import *
from engine.modules.extraction.extraction_module import ExtractionModule
from engine.modules.module import Module


class DummyExtractor(ExtractionModule):
    """
        Genera n records con m columnas y un field por columna
    """

    def __init__(self, **kwargs):
        super(DummyExtractor, self).__init__(**kwargs)
        self.pretty_name = 'DummyExtractor'

    @staticmethod
    def pretty_name():
        return "Dummy"

    def run(self):
        cant_cols = 10
        cant_records = 20

        # se generan los records dummy
        for i in range(cant_records):
            self.records.append(Record())
            for j in range(cant_cols):
                column = Column("Column" + str(j))

                # se añade la columna al esquema de la fuente
                self.add_to_schema(column)

                column.fields.append(Field(
                    value="Val_Rec{0}_col{1}".format(i, j),
                    tipe=FieldType.string
                ))

                self.records[i].columns[column.name] = column

        return self.schema, self.records

    @staticmethod
    def config_json(**kwargs):
        return {
            'config1': {
                'label': 'coso',
                'type': 'text'
            }
        }
