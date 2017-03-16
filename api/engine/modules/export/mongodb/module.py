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

    def __init__(self, **kwargs):
        super(MongoDBExport, self).__init__(**kwargs)
        self.records = records
        self.only_matches = self.config['5_only_matches']['checked'] if "5_only_matches" in self.config and \
                                                                      self.config["5_only_matches"] else False
        self.host = self.config["1_host"] if "1_host" in self.config and self.config["1_host"] else 'localhost'
        self.port = self.config["2_port"] if "2_port" in self.config and self.config["2_port"] else 27017
        self.db = self.config["3_db"] if "3_db" in self.config and self.config["3_db"] else 'output'
        self.collection = self.config["4_collection"] if "4_collection" in self.config and self.config["4_collection"] else 'results'


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
            '1_host': {
                'label': 'Host (default: localhost)',
                'type': 'text'
            },
            '2_port': {
                'label': 'Port (default: 27017)',
                'type': 'text'
            },
            '3_db': {
                'label': 'Database (default: output)',
                'type': 'text'
            },
            '4_collection': {
                'label': 'Collection (default: results)',
                'type': 'text'
            }

            # 'clear_collection': {
            #     'label': 'Clear collection before savinb',
            #     'type': 'checkbox'
            # },
        }
