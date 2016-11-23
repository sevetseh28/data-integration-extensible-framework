from engine.models.record import *
from engine.modules.extraction.extraction_module import ExtractionModule
from engine.modules.module import Module
from pymongo import MongoClient


class MongodbExtractor(ExtractionModule):
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
        super(MongodbExtractor, self).__init__(**kwargs)
        self.pretty_name = 'MongodbExtractor'
        self.host = self.config["host"]
        self.port = self.config["port"]
        self.db = self.config["db"]
        self.collection = self.config["collection"]

    def run (self):
        connection = MongoClient(self.host,self.port)
        db = connection[self.db]
        collection = db[self.collection]
        filters = {}
        extra = {}
        documents = collection.find(filters,extra)
        columns = []
        for doc in documents:
            record = Record()
            for key, value in doc.items():
                if type(value) is int or type(value) is float or type(value) is str:
                    column = Column(key)
                    self.add_to_schema(column)
                    if not [c for c in columns if c.name == key ]:
                        columns.append(column)







