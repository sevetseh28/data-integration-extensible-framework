from engine.models.record import FieldType, Record, Field, Column
from engine.modules.module import Module


class DummyExtractor(Module):

    def __init__(self, **kwargs):
        super(Module, self).__init__(**kwargs)

    def run(self):
        cant_cols = 10
        cant_records = 100

        columns = [Column("Column" + str(i)) for i in range(cant_cols)]

        data = []
        # se generan los records dummy
        for i in range(cant_records):
            data.append(Record())
            for j in range(cant_cols):
                data[i].columns[columns[j]] = [Field(
                    value="val_rec{0}_col{1}".format(i, j),
                    tipe=FieldType.string,
                    column=columns[j]
                )]
        return data
