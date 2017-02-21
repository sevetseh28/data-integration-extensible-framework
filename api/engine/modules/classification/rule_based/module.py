# coding=utf-8
from __future__ import division

import re
from main.models import Project
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
        self.dal = DALMongo(self.project_id)

    @staticmethod
    def pretty_name():
        return "Rule-based classification"

    def run(self, simil):
        #similarity = self.compute_similarity(simil.vector)

        vector = simil.vector
        match_type = MatchResultType.undetermined

        # Given the fact that the simil vector is sorted I must obtain the columns/ofs again from the DAL because
        # the user can send the rules per column/of in any order
        project = Project.objects.get(id=self.project_id)

        cols_order = {}
        if project.segmentation_skipped:
            for idx, c in enumerate(self.dal.get_matched_cols()):
                cols_order[c['name']] = idx
        else:
            for idx, c in enumerate(self.dal.get_output_fields_matched_cols()):
                cols_order[c['name']] = idx


        rules_logical_op = self.logical_operator

        # Initialization of rules total evaluation
        if rules_logical_op == 1:  # apply AND
            rules_evaluation = True
        elif rules_logical_op == 0:
            rules_evaluation = False

        for rule in self.rules:
            col_or_outf_to_compare = rule['output-field-column']['val']
            idx_col_or_outf_to_compare = cols_order[col_or_outf_to_compare]  # index of the simil vector to compare
            logical_op = rule['logical-op']['val']

            if rules_logical_op == 1: # apply AND
                if logical_op == 0: # greater than
                    rules_evaluation = rules_evaluation and rule['value'] < vector[idx_col_or_outf_to_compare]
                elif logical_op == 1:  # less than
                    rules_evaluation = rules_evaluation and rule['value'] > vector[idx_col_or_outf_to_compare]
                elif logical_op == 2:  # equal
                    rules_evaluation = rules_evaluation and rule['value'] == vector[idx_col_or_outf_to_compare]
                elif logical_op == 3:  # equal or greater than
                    rules_evaluation = rules_evaluation and rule['value'] <= vector[idx_col_or_outf_to_compare]
                elif logical_op == 4:  # equal or less than
                    rules_evaluation = rules_evaluation and rule['value'] >= vector[idx_col_or_outf_to_compare]

            elif rules_logical_op == 0: # apply or
                if logical_op == 0: # greater than
                    rules_evaluation = rules_evaluation or rule['value'] < vector[idx_col_or_outf_to_compare]
                elif logical_op == 1:  # less than
                    rules_evaluation = rules_evaluation or rule['value'] > vector[idx_col_or_outf_to_compare]
                elif logical_op == 2:  # equal
                    rules_evaluation = rules_evaluation or rule['value'] == vector[idx_col_or_outf_to_compare]
                elif logical_op == 3:  # equal or greater than
                    rules_evaluation = rules_evaluation or rule['value'] <= vector[idx_col_or_outf_to_compare]
                elif logical_op == 4:  # equal or less than
                    rules_evaluation = rules_evaluation or rule['value'] >= vector[idx_col_or_outf_to_compare]

        match_type = MatchResultType.match if rules_evaluation else MatchResultType.no_match

        return MatchResult(simil.record1, simil.record2, None, match_type)

    @staticmethod
    def _vector_average(vector):
        return sum(vector) / len(vector)

    @staticmethod
    def config_json(project_id):
        # Se cargan las funciones de reduccion del vector
        # vector_reducers = []
        # for func in dir(RuleBasedClassification):
        #     m = re.search('_vector_(.+)', func)
        #     if m:
        #         vector_reducers.append(m.group(1))

        dal = DALMongo(project_id)
        project = Project.objects.get(id=project_id)

        if project.segmentation_skipped:
            cols = [{
                        "label": c['name'],
                        "config": {
                            "val": {
                                'type': 'hidden',
                                'value': c['name'],
                            }
                        }
                    } for c in dal.get_matched_cols()]
        else:
            cols = [{
                        "label": c['name'],
                        "config": {
                            "val": {
                                'type': 'hidden',
                                'value': c['name'],
                            }
                        }
                    } for c in dal.get_output_fields_matched_cols()]

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
                            'config': {
                                "val": {
                                    'type': 'hidden',
                                    'value': 0
                                }
                            }
                        },
                        {
                            'label': 'Less than',
                            'config': {
                                "val": {
                                    'type': 'hidden',
                                    'value': 1
                                }
                            }
                        },
                        {
                            'label': 'Equal to',
                            'config': {
                                "val": {
                                    'type': 'hidden',
                                    'value': 2
                                }
                            }
                        },
                        {
                            'label': 'Greater than or equal to',
                            'config': {
                                "val": {
                                    'type': 'hidden',
                                    'value': 3
                                }
                            }
                        },
                        {
                            'label': 'Less than or equal to',
                            'config': {
                                "val": {
                                    'type': 'hidden',
                                    'value': 4
                                }
                            }
                        }
                    ]
                },
                'value': {
                    "label": "Value",
                    "type": "slider",
                    "start": "0",
                    "end": "1",
                    "step": 0.01,
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


