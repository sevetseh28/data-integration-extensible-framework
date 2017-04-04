# coding=utf-8
from engine.models.record import *
from engine.modules.extraction.extraction_module import ExtractionModule
from engine.modules.module import Module
from pymongo import MongoClient
from datetime import datetime
from copy import deepcopy
from unidecode import unidecode


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
        self.host = self.config["1_host"]
        self.port = int(self.config["2_port"])
        self.db = self.config["3_db"]
        self.collection = self.config["collection"]

    @staticmethod
    def pretty_name():
        return "MongoDB Extractor"

    def run(self):
        connection = MongoClient(self.host, self.port)  # Se crea conexión a db Mongo
        db = connection[self.db]
        collection = db[self.collection]
        documents = collection.find({})
        for doc in documents:  # Se recorren los documentos de la colección para generar todas las columnas
            self.get_all_columns(doc, "")
        documents = collection.find({})
        for i, doc in enumerate(documents):  # Se recorren los documentos nuevamente para obtener los records
            self.records.append(Record())
            for col in self.schema:
                copycol = deepcopy(col)
                colkeys = copycol.name.split(
                    ".")  # En el caso de ser una clave compuesta se itera para acceder al valor
                valuefield = doc
                for k in colkeys:
                    if type(valuefield) is dict:
                        if k in valuefield:
                            valuefield = valuefield[k]
                        else:
                            break
                    else:
                        break
                if type(valuefield) is dict:
                    copycol.fields.append(Field(None, EnumType.notexist))
                else:
                    field = get_field_from_mongo(valuefield)
                    if field is not None:
                        copycol.fields.append(field)
                self.records[i].columns[copycol.name] = copycol
        connection.close()
        return self.schema, self.records

    # Precondición, el documento no tiene claves con algún caracter "."
    def get_all_columns(self, document,
                        concat):  # Se generan las columnas utilizando concatenación con "." en los casos de
        for key, value in document.items():  # documentos embebidos
            key = unidecode(key)
            # Solo se aceptan claves de los siguientes tipos
            if isinstance(value,int) or isinstance(value,long) or isinstance(value, float) or type(
                    value).__name__ == 'Int64' or isinstance(value, str) or isinstance(value, unicode) or isinstance(value, bool) or isinstance(value, datetime) or type(value) is type(None):
                column = Column(concat + key)
                self.add_to_schema(column)
            elif type(value) is dict:
                self.get_all_columns(value, concat + key + ".")  # Si es un dict se concatena la clave con "."
            else:
                continue

    @staticmethod
    def config_json(**kwargs):
        return {
            '1_host': {
                'label': 'Host',
                'type': 'text'
            },
            '2_port': {
                'label': 'Port',
                'type': 'number'
            },
            '3_db': {
                'label': 'Database',
                'type': 'text'
            },
            'collection': {
                'label': 'Collection',
                'type': 'text'
            },
                }


# Se traduce el valor de mongo al formato interno de acuerdo al tipo
def get_field_from_mongo(value):
    if isinstance(value,str):
        return Field(value, EnumType.string)
    elif isinstance(value,unicode):
        return Field(unidecode(value), EnumType.string)
    elif isinstance(value, int) or isinstance(value,long) or isinstance(value,float) or type(value).__name__ == 'Int64':
        return Field(value, EnumType.number)
    elif isinstance(value,bool):
        return Field(value, EnumType.boolean)
    elif isinstance(value,datetime):
        return Field(value, EnumType.date)
    elif type(value) is type(None):
        return Field(value, EnumType.null)
    else:
        return None
