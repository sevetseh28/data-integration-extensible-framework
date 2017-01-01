from __future__ import division
from engine.modules.module import Module
from fuzzywuzzy import fuzz

class TokenSort(Module):
    """
        Applies Token Sort comparison
        >>>fuzz.token_sort_ratio("fuzzy wuzzy was a bear", "wuzzy fuzzy was a bear")
        100
    """

    def __init__(self, **kwargs):
        super(TokenSort, self).__init__(**kwargs)

    @staticmethod
    def pretty_name():
        return "Token Sort"

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
            return fuzz.partial_token_sort_ratio(val1, val2)/100
        else:
            return fuzz.token_sort_ratio(val1, val2)/100
