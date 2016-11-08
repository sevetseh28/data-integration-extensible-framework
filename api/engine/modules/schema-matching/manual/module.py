from engine.dal_mongo import DALMongo
from engine.models.record import *
from engine.modules.module import Module


class ManualSchemaMatching(Module):
    """
    Matchea las columnas de los 2 esquemas 1 a 1 desde comienzo al final del que tenga menos columnas

    Formato de config:
    {
        'matches': [
            {
                'source1': [
                    'colA',
                    'colB',
                    ...
                ],
                'source2': [
                    'colC',
                    'colD',
                    ...
                ]
            },
            ...
        ]
    }
    """

    def __init__(self, project_id, **kwargs):
        super(ManualSchemaMatching, self).__init__(**kwargs)
        self.project_id = project_id
        self.matches = self.config['matches']

    def run(self):
        result = SchemaMatch()

        dal = DALMongo(self.project_id)

        schema1 = {c.name: c for c in dal.get_schema(1)}
        schema2 = {c.name: c for c in dal.get_schema(2)}

        for match in self.matches:
            cols1 = [schema1[col_name] for col_name in match['source1']]
            cols2 = [schema1[col_name] for col_name in match['source2']]

            result.add_match(cols1, cols2)

        return result

    @staticmethod
    def config_json(project_id):
        dal = DALMongo(project_id)

        cols1 = [c.name for c in dal.get_schema(1)]
        cols2 = [c.name for c in dal.get_schema(2)]

        rows = [{
                    'type': 'row',
                    'cols': [
                        {
                            'type': 'select',
                            'options': cols1
                        },
                        {
                            'type': 'select',
                            'options': cols2
                        }
                    ]
                } for _ in range(max(len(cols1), len(cols2)))]

        return {
            'matches': {
                'type': 'rows',
                'rows': rows,
                'label': 'Matches'
            }
        }
