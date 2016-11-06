from engine.dal_mongo import DALMongo
from engine.models.record import *
from engine.modules.indexing.indexing_module import IndexingModule
from engine.modules.module import Module


class BlockingStandard(IndexingModule):
    def __init__(self, records, **kwargs):
        super(BlockingStandard, self).__init__(**kwargs)
        self.records = records
        self.keys = self.config["keys"]

    def run(self):
        groups = {}

        for r in self.records:
            # se obtiene el valor y se codifica
            cols_value = self._concat_cols(r, self.keys)
            encoded_value = self.encode(cols_value)

            # se agrega al conjunto de la clave
            if encoded_value not in groups:
                groups[encoded_value] = []
            groups[encoded_value].append(r)

        return groups

    def _concat_cols(self, record, cols):
        concat = ""
        for col in cols:
            concat += record.columns[col].concat_fields()

        return concat