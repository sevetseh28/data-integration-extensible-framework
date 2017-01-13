import abc
from copy import deepcopy

from engine.models.record import *
from engine.modules.module import Module
from engine.utils.dynamic_loading import load_module
from engine.dal_mongo import DALMongo


class SchemaMatchingModule(Module):
    def __init__(self, **kwargs):
        super(SchemaMatchingModule, self).__init__(**kwargs)
        self.schema = []

    @abc.abstractmethod
    def run(self):
        raise NotImplementedError

    def add_to_schema(self, column, project_id):
        """
        Adds the column to the new schema if it doesnt already exists with the same name.
        If segmentation was applied then the union of the output fields of the matched columns are also included
        """
        if len([c for c in self.schema if c.name == column.name]) > 0:
            return

        dal_mongo = DALMongo(project_id)
        mongoclient = dal_mongo.get_mongoclient()
        db = mongoclient["project{}".format(project_id)]
        coll1 = db["SegmentationStep_source1_schema"]
        coll2 = db["SegmentationStep_source2_schema"]

        # TODO this is done assumming that the format is '__new__cols1-...-__cols2-...'
        # example: column_name = __new__name-surname__nombreyapellido
        matched_columns_s1 = column.name.split('__')[2].split('-') # ['name', 'surname']
        matched_columns_s2 = column.name.split('__')[3].split('-')  # ['nombreyapellido']

        ofs1 = []
        ofs1_type = {}
        for col1 in matched_columns_s1:
            docs = coll1.find({
                'fields': {'$ne' : []},
                'name': col1
            })
            for d in docs:
                for field in d['fields']:
                    f = field['output_field']
                    if f not in ofs1:
                        ofs1.append(f)
                        ofs1_type[f] = field['type']

        ofs2 = []
        ofs2_type = {}
        for col2 in matched_columns_s2:
            docs = coll2.find({
                'fields': {'$ne' : []},
                'name': col2
            })
            for d in docs:
                for field in d['fields']:
                    f = field['output_field']
                    if f not in ofs1:
                        ofs2.append(f)
                        ofs2_type[f] = field['type']


        union_output_fields = list(set().union(ofs1, ofs2))
        union_output_fields_type = ofs1_type.copy()
        union_output_fields_type.update(ofs2_type)

        for of in union_output_fields:
            new_of = Field(tags=[], output_field=of, value="n/A", tipe=EnumType(union_output_fields_type[of])) # type of s1 and s2
                                                                                                    # should be the same
            column.fields.append(new_of)

        self.schema.append(deepcopy(column))
