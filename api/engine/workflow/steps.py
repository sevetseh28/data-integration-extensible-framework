# coding=utf-8
from __future__ import print_function
import logging
from abc import abstractmethod

from engine.dal_mongo import store_step_results
from engine.utils import dynamic_loading

"""
Formato de results:
{
    "collections": [
        {
            "name":"[nombre_col]",
            "values":[array_values]
        },
        ...
    ]
}
"""


class Step(object):
    def __init__(self, project_id, config=None):
        self.results = {
            "collections": []
        }
        self.config = config
        self.class_name = type(self).__name__
        self.project_id = project_id

    """
    run generico. ejecuta cosas previas, ejecuta el step, y ejecuta cosas posteriores
    """

    def run(self):
        logging.info("Starting step " + self.class_name)

        self.run_implementation()

        # se guardan los resultados
        store_step_results(self.project_id, step=self.class_name, results=self.results)

        logging.info("Finished step " + self.class_name)

    """
    firma de el run particular de cada step
    """

    @abstractmethod
    def run_implementation(self):
        pass


"""
Formato del config de extracción:
{
    "source1": {
        "selected_module": {
            "name":"[un_nombre]",
            "config":{[config]}
        }
    },
    "source2": {[idem source1]}
}
"""


class ExtractionStep(Step):
    def __init__(self, **kwargs):
        super(ExtractionStep, self).__init__(**kwargs)
        self.modules_directory = "extraction"

    @staticmethod
    def pretty_name():
        return "Extracción"

    def run_implementation(self):
        module_source_1 = self._load_module(1)
        module_source_2 = self._load_module(2)

        self.results['collections'].append({
            'name': 'source1',
            'values': module_source_1.run()
        })
        self.results['collections'].append({
            'name': 'source2',
            'values': module_source_2.run()
        })

    """
    Carga el modulo dinamicamente
    """

    def _load_module(self, source):
        step = self.modules_directory
        module = self.config['source{}'.format(source)]['selected_module']['name']
        config = self.config['source{}'.format(source)]['selected_module']['config']
        return dynamic_loading.load_module(step, module, config=config)

class StandarizationStep(Step):
     pass
#     def __init__(self):
#         super(StandarizationStep, self).__init__()
#
#     @staticmethod
#     def pretty_name():
#         return "Estandarización"
#
#     def run_implementation(self, config=None):
#         print("Estandarización")
