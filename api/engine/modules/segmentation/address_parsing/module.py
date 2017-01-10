# coding=utf-8
from engine.models.record import *
from engine.modules.module import Module
import re
from engine import global_tags, global_output_fields
from engine.modules.standardisation_tagging.standardisation_tagging_module import StandardisationTaggingModule
class AddressParsing(StandardisationTaggingModule):
    """
        This modules performs a regex search to tokenize an address in address name and address number
        applying a tag for each token group.
    """

    def __init__(self, **kwargs):
        super(AddressParsing, self).__init__(**kwargs)

    @staticmethod
    def pretty_name():
        return 'Address name and number parsing (Uruguay)'

    def run(self, column):
        """
        this module assignes the output field WAYFARE_NAME and WAYFARE_NUMBER to Uruguayan addresses
        :param column: the column with one or more fields and with potentially one or more tags each
        :return: the column with one or more fields and with potentially one or more tags each and an output field
        assigned
        """

        # for each field perform
        #ret_col = Column(name= )
        for idx, field in enumerate(column.fields):
            # it is safe to assume that at this point each field has zero or more tags assigned
            # this module will only assign an output field if a specific tag is encountered on the field
            if global_tags.WN['id'] in field.tags:
                field.output_field = global_output_fields.WAYFARE_NAME
                column.fields[idx] = field
                continue

            if global_tags.N34['id'] in field.tags:
                field.output_field = global_output_fields.WAYFARE_NUMBER
                column.fields[idx] = field
                continue

        return column
