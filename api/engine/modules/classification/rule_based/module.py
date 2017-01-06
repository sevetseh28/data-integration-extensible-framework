# coding=utf-8
from __future__ import division

import re
from engine.dal_mongo import DALMongo
from engine.models.record import *
from engine.modules.classification.classification_module import ClassificationModule
from engine.modules.extraction.extraction_module import ExtractionModule
from engine.modules.module import Module
import operator

class RuleBasedClassification(ClassificationModule):
    """
        Classifies matches based on logical rules applied on the individual compared
        output fields and the total score. Logical operators allowed are AND and OR.

        Formato config:
        {
            rules:[
                '0': {

                },
                '1': {

                }
                ...
            ],
            vector_reducer: <reduce function>
        }
    """

    def __init__(self, project_id, config, **kwargs):
        super(RuleBasedClassification, self).__init__(**kwargs)

        # Si no hay una funcion de reducciond e vector definida, se asigna la de promedio
        if 'vector_reducer' not in self.config:
            self.config['vector_reducer'] = 'average'

        self.compute_similarity = getattr(self, "_vector_" + self.config['vector_reducer'])
        self.project_id = project_id
        self.logical_operator = int(config['logical-op'])
        self.rules = config['rules']

    @staticmethod
    def pretty_name():
        return "Rule-based classification"

    def run(self, simil):
        #similarity = self.compute_similarity(simil.vector)

        vector = simil.vector
        match_type = MatchResultType.undetermined

        # Given the fact that the simil vector is sorted I must obtain the columns/ofs again from the DAL because
        # the user can send the rules per column/of in any order
        dal = DALMongo(self.project_id)

        # TODO Hacer compatible con los output fields
        cols = [{c['name']: idx} for idx, c in enumerate(dal.get_matched_cols())]

        rules_evaluation = False
        for rule in self.rules:
            if self.logical_operator == 1: # apply AND
                pass



        if similarity >= self.upper_bound:
            match_type = MatchResultType.match
        elif similarity < self.lower_bound:
            match_type = MatchResultType.no_match

        return MatchResult(simil.record1, simil.record2, similarity, match_type)

    @staticmethod
    def config_json(project_id):
        # Se cargan las funciones de reduccion del vector
        # vector_reducers = []
        # for func in dir(RuleBasedClassification):
        #     m = re.search('_vector_(.+)', func)
        #     if m:
        #         vector_reducers.append(m.group(1))

        dal = DALMongo(project_id)

        # TODO Hacer compatible con los output fields
        cols = [{'label': c['name'], 'config': {}} for c in dal.get_matched_cols()]

        #for c in cols:


        rowmodel = {
            'type': 'row',
            'cols': {
                'output-field-column': {
                    'label': 'Column/Output Field',
                    'type': 'dropdown',
                    'selectedoption': {},
                    'options': cols
                },
                'logical-op': {
                    'label': 'Operator',
                    'type': 'dropdown',
                    'selectedoption': {},
                    'options': [
                        {
                            'label': 'Greater than',
                            'config': {}
                        },
                        {
                            'label': 'Less than',
                            'config': {}
                        },
                        {
                            'label': 'Equal to',
                            'config': {}
                        },
                        {
                            'label': 'Greater than or equal to',
                            'config': {}
                        },
                        {
                            'label': 'Less than or equal to',
                            'config': {}
                        }
                    ]
                },
                'value': {
                    "label": "Value",
                    "type": "slider",
                    "start": "0",
                    "end": "1",
                    "step": 0.001,
                    "color": "amber"
                }
            }
        }

        return {
            'rules': {
                'type': 'rows',
                'rows': [],
                'label': 'Rules',
                "rowmodel": rowmodel
            },
            'logical-op': {
                'label': 'Logical operator between rules',
                'type': 'radioinline',
                'options': [
                    {
                        'label': 'AND',
                        'value': 1
                    },
                    {
                        'label': 'OR',
                        'value': 0
                    }
                ]
            }
        }

    @staticmethod
    def _vector_average(vector):
        return sum(vector) / len(vector)
