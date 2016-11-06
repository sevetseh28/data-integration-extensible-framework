from engine.dal_mongo import DALMongo
from engine.models.record import *
from engine.modules.module import Module


class FullIndexing(Module):
    """
    Devuelve la agrupacion que es todos con todos
    """

    def __init__(self, records, **kwargs):
        super(FullIndexing, self).__init__(**kwargs)
        self.records = records

    def run(self):
        return {'all': self.records}
