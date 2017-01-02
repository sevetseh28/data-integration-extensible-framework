from __future__ import division

from engine.modules.comparison.comparison_module import ComparisonModule
from engine.modules.module import Module
from fuzzywuzzy import fuzz

class Ratio(ComparisonModule):
    """
        Applies Ratio comparison
        >>>fuzz.ratio("this is a test", "this is a test!")
        97
        >>>fuzz.partial_ratio("this is a test", "this is a test!")
        100
    """

    def __init__(self, **kwargs):
        super(Ratio, self).__init__(**kwargs)

    @staticmethod
    def pretty_name():
        return "Ratio"

    @staticmethod
    def config_json(**kwargs):
        return {
            'partial': {
                'type': 'toggleswitch',
                'label': 'Partial',
                "color": 'green'
            }
        }

    def run(self, val1, val2):
        if self.config['partial']['checked']:
            return fuzz.partial_ratio(val1, val2)/100
        else:
            return fuzz.ratio(val1, val2)/100
