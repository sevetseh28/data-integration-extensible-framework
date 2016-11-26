# coding=utf-8
from engine.models.record import *
from engine.modules.extraction.extraction_module import ExtractionModule
from engine.modules.module import Module
from pymongo import MongoClient
from datetime import datetime
from copy import deepcopy



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

    def run(self):
        connection = MongoClient(self.host,self.port) #Se crea conexión a db Mongo
        db = connection[self.db]
        collection = db[self.collection]
        documents = collection.find({})
        for doc in documents:  #Se recorren los documentos de la colección para generar todas las columnas
            self.get_all_columns(doc,"")
        documents = collection.find({})
        for i,doc in enumerate(documents): #Se recorren los documentos nuevamente para obtener los records
            self.records.append(Record())
            for col in self.schema:
                copycol = deepcopy(col)
                colkeys = copycol.name.split(".") #En el caso de ser una clave compuesta se itera para acceder al valor
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
                    copycol.fields.append(Field(None,FieldType.notexist))
                else:
                    field = get_field_from_mongo(valuefield)
                    if field is not None:
                        copycol.fields.append(field)
                self.records[i].columns[copycol.name] = copycol
        connection.close()
        return self.schema, self.records






#Precondición, el documento no tiene claves con algún caracter "."
    def get_all_columns(self,document,concat): #Se generan las columnas utilizando concatenación con "." en los casos de
        for key,value in document.items():  #documentos embebidos
            #Solo se aceptan claves de los siguientes tipos
            if type(value) is int or type(value) is long or type(value) is float or type(value) is str or type(value) is unicode or type(value) is bool or type(value) is datetime or type(value) is type(None):
                column = Column(concat+key)
                self.add_to_schema(column)
            elif type(value) is dict:
                self.get_all_columns(value,concat+key+".") #Si es un dict se concatena la clave con "."
            else:
                continue

#Se traduce el valor de mongo al formato interno de acuerdo al tipo
def get_field_from_mongo(value):
    if type(value) is str or type(value) is unicode:
        return Field(value, FieldType.string)
    elif type(value) is int or type(value) is long or type(value) is float:
        return Field(value, FieldType.number)
    elif type(value) is bool:
        return Field(value, FieldType.boolean)
    elif type(value) is datetime:
        return Field(value, FieldType.date)
    elif type(value) is type(None):
        return Field(value,FieldType.null)
    else:
        return None












