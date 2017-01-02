# coding=utf-8
from engine.models.record import *
from engine.modules.comparison.comparison_module import ComparisonModule
from engine.modules.extraction.extraction_module import ExtractionModule
from engine.modules.module import Module


class EqualsComparison(ComparisonModule):
    """
        Devuelve 1 si son iguales y 0 si no
    """

    def __init__(self, **kwargs):
        super(EqualsComparison, self).__init__(**kwargs)

    @staticmethod
    def pretty_name():
        return "Equal"

    def run(self, val1, val2):
        return int(val1 == val2)
