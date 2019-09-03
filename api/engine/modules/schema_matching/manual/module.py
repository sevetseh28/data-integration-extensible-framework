# coding=utf-8
from engine.dal_mongo import DALMongo
from engine.models.record import *
from engine.modules.module import Module
from engine.modules.schema_matching.schema_matching_module import SchemaMatchingModule


class ManualSchemaMatching(SchemaMatchingModule):
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
        self.deduplicate_custom_names()
        self.remaining_columns = self.config['remaining_columns']['checked'] if "remaining_columns" in self.config \
                                                                        and self.config["remaining_columns"] else False

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

            schematches.add_match(cols1, cols2, match['custom_name'])

        # Schemas are standardised
        self.records1 = self._standardise_schema(self.records1, schematches, 1, schema2)
        self.records2 = self._standardise_schema(self.records2, schematches, 2, schema1)

        # Create the global schema
        # taking one record and getting the matched schema will be enough
        for col_name, col_obj in self.records1[0].columns.items():
            if col_name.startswith("__new__") or self.remaining_columns:
                self.add_to_schema(Column(col_name, [], col_obj.type, col_obj.is_new, col_obj.custom_name),
                                   self.project_id)
        return self.schema, self.records1, self.records2

    def _standardise_schema(self, records, schematches, source_number, other_schema):
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
                r.join_cols(match["source{}".format(source_number)], match["col_name"], match['custom_name'])

            # Se eliminan las columnas que correspondian a los matcheos
            for match in schematches.schema_matches:
                r.remove_cols(match["source{}".format(source_number)])

            if self.remaining_columns:
                # Se pone prefijo a las columnas propias de este esquema para identificarlas
                r.prefix_cols("s{}".format(source_number))

                # Se añaden las columnas del otro esquema
                for col in extra_cols:
                    r.add_column(Column(col))
            else:
                r.remove_nonmatched_cols()

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
                    'label': 'Select source 1 columns',
                    'type': 'multipleselect',
                    'options': cols1
                },
                'source2': {
                    'label': 'Select source 2 columns',
                    'type': 'multipleselect',
                    'options': cols2
                },
                'custom_name': {
                    'label': 'New column name',
                    'type': 'text'
                }
            }
        }

        return {
            'matches': {
                'type': 'rows',
                'rows': [],
                'label': 'Matches',
                "rowmodel": rowmodel
            },
            'remaining_columns': {
                'label': 'Add remaining columns to the final schema',
                'type': 'toggleswitch',
                "color": 'blue',
                'checked': False
            },
        }

    def deduplicate_custom_names(self):
        while len({m['custom_name']: None for m in self.matches}) < len(self.matches):

            matches = {i: self.matches[i] for i in range(len(self.matches))}
            matches2 = {i: self.matches[i] for i in range(len(self.matches))}

            for (i, m) in matches.items():
                suffix_count = 1

                matches2.pop(i)
                for (j, m2) in matches2.items():
                    if m['custom_name'] == m2['custom_name']:
                        m2['custom_name'] = "{}_{}".format(m2['custom_name'], suffix_count)
                        suffix_count += 1
