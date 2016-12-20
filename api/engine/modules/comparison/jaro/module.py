from __future__ import division
from engine.modules.module import Module
import Levenshtein


class JaroComparison(Module):
    """
        Applies the Jaro string comparison function
    """

    def __init__(self, **kwargs):
        super(JaroComparison, self).__init__(**kwargs)

    @staticmethod
    def pretty_name():
        return "Jaro"

    @staticmethod
    def config_json(**kwargs):
        return {}

    def run(self, val1, val2):
        return Levenshtein.jaro(val1, val2)