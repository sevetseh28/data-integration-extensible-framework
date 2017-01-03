# coding=utf-8
from engine.models.record import *
from engine.modules.module import Module
from engine.modules.standardisation_tagging.standardisation_tagging_module import StandardisationTaggingModule


class DummyStandardisationAndTagging(StandardisationTaggingModule):
    """
        T
    """

    def __init__(self, **kwargs):
        super(DummyStandardisationAndTagging, self).__init__(**kwargs)

    @staticmethod
    def pretty_name():
        return 'Dummy'

    def run(self, column):
        """

        :param column:
        :return:
        """
        # column should have one field at this point representing all the column, we will asign only
        # one tag 'Unknown' to all this field
        column.fields[0].tags.append('Unknown')
        return column