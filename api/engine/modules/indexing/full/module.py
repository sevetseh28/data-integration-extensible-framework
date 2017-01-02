from engine.modules.indexing.indexing_module import IndexingModule
from engine.modules.module import Module


class FullIndexing(IndexingModule):
    """
    Devuelve la agrupacion que es todos con todos
    """

    def __init__(self, records, **kwargs):
        super(FullIndexing, self).__init__(**kwargs)
        self.records = records

    @staticmethod
    def pretty_name():
        return "Full index"

    def run(self):
        return {'all': self.records}
