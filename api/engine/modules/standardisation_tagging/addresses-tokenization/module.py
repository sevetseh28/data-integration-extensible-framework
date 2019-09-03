# coding=utf-8
from engine.models.record import *
from engine.modules.module import Module
import re
from engine import global_tags
from engine.modules.standardisation_tagging.standardisation_tagging_module import StandardisationTaggingModule


class AddressesTokenization(StandardisationTaggingModule):
    """
        This modules performs a regex search to tokenize an address in address name and address number
        applying a tag for each token group.
    """

    def __init__(self, **kwargs):
        super(AddressesTokenization, self).__init__(**kwargs)

    @staticmethod
    def pretty_name():
        return 'Address name and number tagging (Uruguay)'

    def run(self, column):
        """

        :param column: is it assumed that at this point the column comes with only one field
        :return: the column with one or more fields and with potentially one or more tags
        """
        field_value = column.fields[0].value

        regex_name = '^(.+)\s(\d{3,4}).*$'
        regex_number = '(\d{3,4})+'
        matches_name = re.search(regex_name, field_value)
        matches_number = re.search(regex_number, field_value)

        address_name = matches_name.group(1) if matches_name is not None else ""
        address_number = matches_number.group(1) if matches_number is not None else ""

        fields = []
        if address_name != "":
            address_name_field = Field(address_name, EnumType.string, tags=[global_tags.WN['id']],
                                       output_field=None)
            fields.append(address_name_field)

        # only append number if it was found
        if address_number != "":
            address_number_field = Field(address_number, EnumType.number, tags=[global_tags.N34['id']],
                                         output_field=None)
            fields.append(address_number_field)

        if len(fields) == 0:  # if an empty string was found in the column return the same column
            return column
        else:
            # Create the return column object
            ret_column = Column(name=column.name, fields=fields)
            return ret_column
