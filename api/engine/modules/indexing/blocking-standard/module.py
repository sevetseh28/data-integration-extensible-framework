from unidecode import unidecode

from engine.dal_mongo import DALMongo
from engine.modules.indexing.indexing_module import IndexingModule
from engine.modules.module import Module
from engine.utils import dynamic_loading
from engine.utils.dynamic_loading import load_module


class BlockingStandard(IndexingModule):
    """
    Formato config:
    {
        'keys': [
            'key1',
            'key2',
            ...
        ],
        'encoding':{
            'name':'[name]',
            'config': {}
        }
    }
    """

    def __init__(self, records, **kwargs):
        super(BlockingStandard, self).__init__(**kwargs)
        self.records = records
        self.keys = [{"key": unidecode(k["key"]["key"]), "encoding": k["encoding"]} for k in self.config["keys"]]

        # encodings attribute will mantain all selected encoding modules
        self.encodings = {}
        for ke in self.config["keys"]:
            if ke["encoding"]["name"] not in self.encodings:
                self.encodings[ke["encoding"]["name"]] = load_module("encoding", ke['encoding']['name'],
                                                             config=ke['encoding'])

    @staticmethod
    def pretty_name():
        return "Blocking Standard"

    def run(self):
        groups = {}

        for r in self.records:
            # se obtiene el valor y se codifica
            cols_value_encoded = self._concat_cols(r)

            # se agrega al conjunto de la clave
            if cols_value_encoded not in groups:
                groups[cols_value_encoded] = []
            groups[cols_value_encoded].append(r)

        return groups

        # @staticmethod

    def _concat_cols(self, record):
        concat = ""
        for ke in self.keys:
            concat += self.encodings[ke["encoding"]["name"]].run(str(record.columns[ke["key"]].concat_fields()))
        return concat

    @staticmethod
    def config_json(project_id):
        dal = DALMongo(project_id)

        cols = [{
                    "label": c,
                    "value": c,
                    "id": c,
                    "config": {
                        "key": {
                            'type': 'hidden',
                            'value': c,
                        }
                    }
                } for c in dal.get_global_schema() if c.startswith('__new__')]
        # TODO arreglar la porqueria de arriba con el __new__ hardcodeado

        encoding_configs = dynamic_loading.list_modules('encoding')

        rowmodel = {
            'type': 'row',
            'cols': {
                'key':
                    {
                        'type': 'dropdown',
                        'label': 'Select a column',
                        'selectedoption': {},
                        'options': cols
                    },
                'encoding':
                    {
                        "type": "dropdown",
                        'label': 'Select encoding',
                        'selectedoption': {},
                        'options': encoding_configs
                    }
            }
        }
        return {
            'keys': {
                'type': 'rows',
                'rows': [],
                'label': 'Keys',
                "rowmodel": rowmodel
            }
        }

        # return {
        #     'keys': {
        #         'type': 'multipleselect',
        #         'options': cols,
        #         'label': 'Keys'
        #     },
        #     'encoding': {
        #         "type": "dropdown",
        #         'label': 'Select encoding',
        #         'selectedoption': {},
        #         'options': encoding_configs
        #     }
        # }

        # @staticmethod
        # def config_json(**kwargs):
        #     return {
        #         'keys': {
        #             'label': 'Keys',
        #             'type': 'list'
        #         },
        #         'encoding': {
        #             'label': 'Encoding',
        #             'type': 'select',
        #             'options': dynamic_loading.list_modules('encoding')
        #         }
        #     }
