from pymongo import MongoClient

from engine.modules.indexing.indexing_module import IndexingModule
from engine.modules.module import Module
from engine.utils import dynamic_loading


class MongoDBExport(IndexingModule):
    """
    Formato config:
    {
        'host': "[host]",
        'port': "[port]",
        'db': "[db]",
        'collection': "[collection]",
    }
    """

    def __init__(self, records, **kwargs):
        super(MongoDBExport, self).__init__(**kwargs)
        self.records = records
        self.host = self.config["host"]
        self.port = self.config["port"]
        self.db = self.config["db"]
        self.collection = self.config["collection"]

    @staticmethod
    def pretty_name():
        return "MongoDB"

    def run(self):
        json_values = [r.to_json() for r in self.records]

        connection = MongoClient(self.host, int(self.port))
        connection[self.db][self.collection].insert_many(json_values)
        connection.close()

    @staticmethod
    def config_json(**kwargs):
        return {
            'host': {
                'label': 'Host',
                'type': 'text'
            },
            'port': {
                'label': 'Port',
                'type': 'text'
            },
            'db': {
                'label': 'Database',
                'type': 'text'
            },
            'collection': {
                'label': 'Collection',
                'type': 'text'
            },
        }
