# coding=utf-8
from engine.models.record import *
from engine.modules.module import Module
import re
from engine import global_tags, global_output_fields
from engine.modules.segmentation.segmentation_module import SegmentationModule

class NamesParsing(SegmentationModule):
    """
    """

    def __init__(self, **kwargs):
        super(NamesParsing, self).__init__(**kwargs)

    @staticmethod
    def pretty_name():
        return 'Names parsing'

    def run(self, column):
        """
        :param column: the column with one or more fields and with potentially one or more tags each
        :return: the column with one or more fields and with potentially one or more tags each and an output field
        assigned
        """

        # for each field perform
        #ret_col = Column(name= )
        total_fields = len(column.fields)
        state = 0
        # 0 nothing found
        # 1 found first name
        # 2 found second name

        for idx, field in enumerate(column.fields):
            # it is safe to assume that at this point each field has zero or more tags assigned
            if global_tags.GN['id'] in field.tags:
                if state == 0:
                    field.output_field = global_output_fields.FIRST_NAME
                    state = 1
                elif state == 1:
                    field.output_field = global_output_fields.SECOND_NAME
                    state = 2
            elif global_tags.SN['id'] in field.tags:
                field.output_field = global_output_fields.SURNAME

            column.fields[idx] = field

        return column
