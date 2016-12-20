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
        self.keys = [{"key": unidecode(k["key"]), "encoding": k["encoding"]} for k in self.config["keys"]]
        self.encodings = {}
        for ke in self.config["keys"]:
            if ke["encoding"] not in self.encodings:
                self.encodings[ke["encoding"]] = load_module("encoding", ke['encoding']['name'],
                                                             config=ke['encoding'])

    @staticmethod
    def pretty_name():
        return "Blocking Standard"

    def run(self):
        groups = {}

        for r in self.records:
            # se obtiene el valor y se codifica
            cols_value_encoded = self._concat_cols(r, self.keys)

            # se agrega al conjunto de la clave
            if cols_value_encoded not in groups:
                groups[cols_value_encoded] = []
            groups[cols_value_encoded].append(r)

        return groups

        # @staticmethod

    def _concat_cols(self, record):
        concat = ""
        for ke in self.keys:
            for field in record.columns[ke["key"]].fields:
                concat += self.encodings[ke["encoding"]].run(str(field.value))
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
