# coding=utf-8
from engine.dal_mongo import DALMongo
from engine.models.record import *
from engine.modules.module import Module


class ManualSchemaMatching(Module):
    """
    Genera el matcheo manual
    Estandariza los registros para un esquema global que tiene las columnas matcheadas y las no matcheadas con valores null

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

    def __init__(self, project_id, records1, records2, **kwargs):
        super(ManualSchemaMatching, self).__init__(**kwargs)
        self.records1 = records1
        self.records2 = records2
        self.project_id = project_id

        self.matches = self.config['matches']

    @staticmethod
    def pretty_name():
        return "Manual matching"

    def run(self):
        schematches = SchemaMatch()

        dal = DALMongo(self.project_id)

        # se obtienen las columnas originales
        schema1 = {c.name: c for c in dal.get_schema(1)}
        schema2 = {c.name: c for c in dal.get_schema(2)}

        # se crea un obj SchemaMatch con los pares de columans elegidos
        for match in self.matches:
            cols1 = [schema1[col_name] for col_name in match['source1']]
            cols2 = [schema2[col_name] for col_name in match['source2']]

            schematches.add_match(cols1, cols2)

        # Se estandarizadn los esquemas
        self.records1 = self._estandarize_schema(self.records1, schematches, 1, schema2)
        self.records2 = self._estandarize_schema(self.records2, schematches, 2, schema1)

        return self.records1, self.records2

    @staticmethod
    def _estandarize_schema(records, schematches, source_number, other_schema):
        # Estas son las columnas del otro esquema. Quedaran vacias en los registros de este esquema
        extra_cols = [col.name for col in other_schema.values()]
        other_source_number = 1 if source_number == 2 else 2

        # Se sacan de las extra cols, las columnas que estan matcheadas, para que no queden duplicadas
        for match in schematches.schema_matches:
            match_cols = [c.name for c in match["source{}".format(other_source_number)]]
            extra_cols = [col for col in extra_cols if col not in match_cols]

        # Se renombran las columans del otro esquema con un prefijo para identificarlas
        extra_cols = ["s{}_{}".format(other_source_number, col) for col in extra_cols]

        for r in records:
            # Se unifican las columnas de cada matcheo de esquemas
            for match in schematches.schema_matches:
                r.join_cols(match["source{}".format(source_number)], match["col_name"])

            # Se eliminan las columnas que correspondian a los matcheos
            for match in schematches.schema_matches:
                r.remove_cols(match["source{}".format(source_number)])

            # Se pone prefijo a las columnas propias de este esquema para identificarlas
            r.prefix_cols("s{}".format(source_number))

            # Se añaden las columnas del otro esquema
            for col in extra_cols:
                r.add_column(Column(col))

        return records

    @staticmethod
    def config_json(project_id):
        dal = DALMongo(project_id)

        cols1 = [c.name for c in dal.get_schema(1)]
        cols2 = [c.name for c in dal.get_schema(2)]

        rowmodel = {
            'type': 'row',
            'cols': {
                'source1': {
                    'type': 'multipleselect',
                    'options': cols1
                },
                'source2': {
                    'type': 'multipleselect',
                    'options': cols2
                }
            }
        }

        return {
            'matches': {
                'type': 'rows',
                'rows': [],
                'label': 'Matches',
                "rowmodel": rowmodel
            }
        }
