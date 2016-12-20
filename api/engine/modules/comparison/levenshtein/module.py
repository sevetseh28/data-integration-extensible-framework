from __future__ import division
from engine.modules.module import Module
import Levenshtein


class LevenshteinDistance(Module):
    """
        Applies Levenshtein edit distance and returns a value between 0 and 1
    """

    def __init__(self, **kwargs):
        super(LevenshteinDistance, self).__init__(**kwargs)

    @staticmethod
    def pretty_name():
        return "Levenshtein distance"

    @staticmethod
    def config_json(**kwargs):
        return {}

    def run(self, val1, val2):
        lev_distance = Levenshtein.distance(val1, val2)
        max_length = max(len(val1), len(val2))
        return (1.0 - lev_distance/max_length)