from engine.models.record import *
from engine.modules.module import Module

"""
    Genera n records con m columnas y un field por columna
"""
class DummyExtractor(Module):
    def __init__(self, **kwargs):
        super(DummyExtractor, self).__init__(**kwargs)

    def run(self):
        cant_cols = 10
        cant_records = 100

        columns = [Column("Column" + str(i)) for i in range(cant_cols)]

        schema = columns
        records = []

        # se generan los records dummy
        for i in range(cant_records):
            records.append(Record())
            for j in range(cant_cols):
                records[i].columns[columns[j]] = [Field(
                    value="val_rec{0}_col{1}".format(i, j),
                    tipe=FieldType.string,
                    column=columns[j]
                )]
        return schema, records
