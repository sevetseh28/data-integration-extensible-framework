import time

from engine.dal_mongo import DALMongo
from engine.models.record import Record, Column
from engine.modules.module import Module
from engine.utils import dynamic_loading


class PreferredSource(Module):
    """
    Formato config:
    {
        'preferred-source': [1|2]
    }
    """

    def __init__(self, project_id, matches, **kwargs):
        super(PreferredSource, self).__init__(**kwargs)
        self.project_id = project_id
        self.matches = matches
        self.preferred_source = self.config["preferred-source"]

    @staticmethod
    def pretty_name():
        return "Preferred source"

    def run(self):
        dal = DALMongo(self.project_id)

        fused_records = []
        for match in self.matches:
            # se obtienen los registros matcheados
            [r1, r2] = dal.get_match_pair(match)

            # se extraen las columnas que no estan matcheadas
            r1_remaining_cols = r1.get_sourcex_cols(1)
            r2_remaining_cols = r2.get_sourcex_cols(2)

            # se crea un record con las columnas no matcheadas
            r3 = Record(id=match._id)
            r3.add_columns(r1_remaining_cols)
            r3.add_columns(r2_remaining_cols)

            # se agregan las columnas matcheadas de acuerdo al criterio
            preferred_record = r1 if self.preferred_source == 1 else r2
            for col in preferred_record.get_new_cols():
                r3.add_column(col)

            fused_records.append(r3)

        return fused_records

    @staticmethod
    def config_json(**kwargs):
        return {
            'preferred-source': {
                'label': 'Select the preferred source',
                'type': 'radio',
                'options': [
                    {"value": 1, "label": "Source 1"},
                    {"value": 2, "label": "Source 2"}
                ]
            }
        }

    def column_from_schmatch(self, preferred_record, schmatch):
        cols = schmatch["source1"] if self.preferred_source == 1 else schmatch["source2"]

        col_name = cols[0].name
        fields = preferred_record.columns[cols[0].name].fields
        for col in cols[1:]:
            col_name += "-{}".format(col.name)
            fields += preferred_record.columns[col.name].fields

        return Column(col_name, fields)

    @staticmethod
    def _get_unmatched_cols(schematches, schema1, schema2):
        schema1 = [c.name for c in schema1]
        schema2 = [c.name for c in schema2]

        for schmatch in schematches.schema_matches:
            matched_cols1 = [c.name for c in schmatch["source1"]]
            matched_cols2 = [c.name for c in schmatch["source2"]]

            schema1 = [s for s in schema1 if s not in matched_cols1]
            schema2 = [s for s in schema2 if s not in matched_cols2]

        return schema1, schema2
