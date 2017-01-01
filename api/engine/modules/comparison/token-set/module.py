from __future__ import division
from engine.modules.module import Module
from fuzzywuzzy import fuzz

class TokenSet(Module):
    """
        Applies Token Set comparison
        >>>fuzz.token_set_ratio("fuzzy was a bear", "fuzzy fuzzy was a bear")
        100
    """

    def __init__(self, **kwargs):
        super(TokenSet, self).__init__(**kwargs)

    @staticmethod
    def pretty_name():
        return "Token Set"

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
