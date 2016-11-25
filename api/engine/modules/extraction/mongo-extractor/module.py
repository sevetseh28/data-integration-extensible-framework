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
            self.get_all_columns(doc,"")
        for doc in documents:
            self.records.append(Record())
            for col in self.schema:
                colkeys = col.name.split(".")
                valuedoc = doc
                for k in colkeys:
                    if type(valuedoc) is dict:
                        if valuedoc[k]:
                            valuedoc = valuedoc[k]
                        else:
                            valuedoc = Enum.









    def get_all_columns(self,document,concat):
        for key,value in document.items():
            if type(value) is int or type(value) is float or type(value) is str:
                column = Column(concat+key)
                self.add_to_schema(column)
            elif type(value) is dict:
                concat += key+"."
                self.get_all_columns(value,concat)
            else:
                continue











