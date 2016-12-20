from __future__ import division
from engine.modules.module import Module
import Levenshtein


class JaroWinklerComparison(Module):
    """
        Applies the Jaro-Winkler string comparison function
    """

    def __init__(self, **kwargs):
        super(JaroWinklerComparison, self).__init__(**kwargs)

    @staticmethod
    def pretty_name():
        return "Jaro-Winkler"

    @staticmethod
    def config_json(**kwargs):
        return {}

    def run(self, val1, val2):
        return Levenshtein.jaro_winkler(val1, val2)