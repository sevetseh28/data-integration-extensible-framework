# coding=utf-8
from engine.models.record import *
from engine.modules.module import Module
import re
from engine import global_tags, global_output_fields
from engine.modules.segmentation.segmentation_module import SegmentationModule

class UniqueSegmentAssignment(SegmentationModule):
    """
        This modules performs a regex search to tokenize an address in address name and address number
        applying a tag for each token group.
    """

    def __init__(self, **kwargs):
        super(UniqueSegmentAssignment, self).__init__(**kwargs)

    @staticmethod
    def pretty_name():
        return 'Unique segment assignment'

    def run(self, column):
        """
        this module assignes the custom output field specified by the user to the column
        :param column: the column with one or more fields and with potentially one or more tags each
        :return: the column with one field and with the union of the tags that it originally had. The outputfield is
        the one specified by the user
        """

        # for each field perform
        tags_in_fields = []
        column_value = column.concat_fields()
        for field in column.fields:
            # get all tags of all fields in one list
            tags_in_fields.extend(field.tags)

        # create the new single field
        field = Field(value=column_value, tags=tags_in_fields, output_field=self.config['custom_of'], tipe=EnumType(1))

        column_ret = Column(column.name, fields=[field], type=column.type)

        return column_ret



    @staticmethod
    def config_json(**kwargs):
        return {
            'custom_of': {
                "type": "text",
                "label": "Custom output field to assign"
            }
        }