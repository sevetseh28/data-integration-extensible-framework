# coding=utf-8
from __future__ import division

import re

from engine.models.record import *
from engine.modules.extraction.extraction_module import ExtractionModule
from engine.modules.module import Module


class FellegiSunterClassification(Module):
    """
        Devuelve
            - match si la similitud esta por encima de upper bound
            - indeterminado si la similitud esta entre la upper y lower
            - no match si la similitud esta por debajo de la lower bound

        Formato config:
        {
            "lower_bound": [numero],
            "upper_bound": [numero],
            "vector_reducer": [funcion de reduccion]
        }
    """

    def __init__(self, **kwargs):
        super(FellegiSunterClassification, self).__init__(**kwargs)

        # Si no hay una funcion de reducciond e vector definida, se asigna la de promedio
        if 'vector_reducer' not in self.config:
            self.config['vector_reducer'] = 'average'

        self.compute_similarity = getattr(self, "_vector_" + self.config['vector_reducer'])

        self.lower_bound = self.config['lower_bound']
        self.upper_bound = self.config['upper_bound']

    @staticmethod
    def pretty_name():
        return "Fellegi Sunter"

    def run(self, simil):
        similarity = self.compute_similarity(simil.vector)

        match_type = MatchResultType.undetermined
        if similarity >= self.upper_bound:
            match_type = MatchResultType.match
        elif similarity < self.lower_bound:
            match_type = MatchResultType.no_match

        return MatchResult(simil.record1, simil.record2, similarity, match_type)

    @staticmethod
    def config_json(**kwargs):
        # Se cargan las funciones de reduccion del vector
        vector_reducers = []
        for func in dir(FellegiSunterClassification):
            m = re.search('_vector_(.+)', func)
            if m:
                vector_reducers.append(m.group(1))

        return {
            'thresholds': {
                "type": "rangeslider",
                "label": "Range for potential matches",
                "start": "0",
                "end": "1",
                "from": "0.5",
                "to": "0.7",
                "step": 0.01
            },
            # 'vector_reducer': {
            #     'type': 'select',
            #     'label': 'Vector reducer',
            #     'options': vector_reducers
            # }
        }

    @staticmethod
    def _vector_average(vector):
        return sum(vector) / len(vector)
