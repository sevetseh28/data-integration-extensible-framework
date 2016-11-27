from engine.dal_mongo import DALMongo
from engine.modules.indexing.indexing_module import IndexingModule
from engine.modules.module import Module
from engine.utils import dynamic_loading


class BlockingStandard(IndexingModule):
    """
    Formato config:
    {
        'keys': [
            'key1',
            'key2',
            ...
        ]
    }
    """

    def __init__(self, records, **kwargs):
        super(BlockingStandard, self).__init__(**kwargs)
        self.records = records
        self.keys = self.config["keys"]

    @staticmethod
    def pretty_name():
        return "Blocking Standard"

    def run(self):
        groups = {}

        for r in self.records:
            # se obtiene el valor y se codifica
            cols_value = self._concat_cols(r, self.keys)
            encoded_value = self.encode(cols_value)

            # se agrega al conjunto de la clave
            if encoded_value not in groups:
                groups[encoded_value] = []
            groups[encoded_value].append(r)

        return groups

    @staticmethod
    def _concat_cols(record, cols):
        concat = ""
        for col in cols:
            concat += record.columns[col].concat_fields()

        return concat

    @staticmethod
    def config_json(project_id):
        dal = DALMongo(project_id)

        cols1 = [c.name for c in dal.get_schema(1)]
        cols2 = [c.name for c in dal.get_schema(2)]

        encoding_configs = dynamic_loading.list_modules('encoding')

        rowmodel = {
            'type': 'row',
            'cols': [
                {
                    'type': 'dropdown',
                    'label': 'Select a column',
                    'selectedoption': {},
                    'options': cols1
                },
                {
                    "type": "dropdown",
                    'label': 'Select encoding',
                    'selectedoption': {},
                    'options': encoding_configs
                }
            ]
        }

        return {
            'keys': {
                'type': 'rows',
                'rows': [],
                'label': 'Keys',
                "rowmodel": rowmodel
            }
        }

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
