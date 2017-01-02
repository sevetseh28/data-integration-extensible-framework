from pymongo import MongoClient

from engine.modules.export.export_module import ExportModule
from engine.modules.indexing.indexing_module import IndexingModule
from engine.modules.module import Module
from engine.utils import dynamic_loading


class MongoDBExport(ExportModule):
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
        self.host = self.config["host"] if "host" in self.config and self.config["host"] else 'localhost'
        self.port = self.config["port"] if "port" in self.config and self.config["port"] else 27017
        self.db = self.config["db"] if "db" in self.config and self.config["db"] else 'output'
        self.collection = self.config["collection"] if "collection" in self.config and self.config["collection"] else 'results'


    @staticmethod
    def pretty_name():
        return "MongoDB"

    def run(self):
        json_values = [r.to_json() for r in self.records]

        connection = MongoClient(self.host, int(self.port))

        # if self.config["clear_collection"]:
        #     connection[self.db][self.collection].drop()

        connection[self.db][self.collection].insert_many(json_values)
        connection.close()

    @staticmethod
    def config_json(**kwargs):
        return {
            'host': {
                'label': 'Host (default: localhost)',
                'type': 'text'
            },
            'port': {
                'label': 'Port (default: 27017)',
                'type': 'text'
            },
            'db': {
                'label': 'Database (default: output)',
                'type': 'text'
            },
            'collection': {
                'label': 'Collection (default: results)',
                'type': 'text'
            },
            # 'clear_collection': {
            #     'label': 'Clear collection before savinb',
            #     'type': 'checkbox'
            # },
        }
