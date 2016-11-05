# coding=utf-8
from __future__ import print_function
import logging
from abc import abstractmethod

from engine.dal_mongo import DALMongo
from engine.utils import dynamic_loading


class Step(object):
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

    def __init__(self, project_id=None, config=None):
        self.results = {
            "collections": []
        }
        self.config = config
        self.class_name = type(self).__name__
        self.project_id = project_id
        self.modules_directory = None

    def run(self):
        """
        Run generico. ejecuta cosas previas, ejecuta el step, y ejecuta cosas posteriores
        """
        logging.info("Starting step " + self.class_name)

        self.run_implementation()

        # se guardan los resultados
        dal = DALMongo(self.project_id)
        dal.store_step_results(step=self.class_name, results=self.results)

        logging.info("Finished step " + self.class_name)

    @abstractmethod
    def run_implementation(self):
        """
        Firma de el run particular de cada step
        """
        pass

    @staticmethod
    @abstractmethod
    def pretty_name():
        pass

    def _load_module(self, **kwargs):
        """
        Carga el modulo dinamicamente.
        Implementación por defecto
        """
        step = self.modules_directory
        module = self.config['selected_module']['name']
        config = self.config['selected_module']['config']
        return dynamic_loading.load_module(step, module, config=config, **kwargs)

    def _append_result_collection(self, values, collection_suffix=''):
        """
        Appendea una coleccion a los resultados
        """
        self.results['collections'].append({
            'name_suffix': collection_suffix,
            'values': values
        })


class ExtractionStep(Step):
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

    def __init__(self, **kwargs):
        super(ExtractionStep, self).__init__(**kwargs)
        self.modules_directory = "extraction"

    @staticmethod
    def pretty_name():
        return "Extraction"

    def run_implementation(self):
        self._load_module_results(1)
        self._load_module_results(2)

    def _load_module(self, source):
        step = self.modules_directory
        module = self.config['source{}'.format(source)]['selected_module']['name']
        config = self.config['source{}'.format(source)]['selected_module']['config']
        return dynamic_loading.load_module(step, module, config=config)

    def _load_module_results(self, source_number):
        module = self._load_module(source_number)
        (schema, records) = module.run()

        self._append_result_collection(records, 'source{}_records'.format(source_number))
        self._append_result_collection(schema, 'source{}_schema'.format(source_number))


class StandardizationStep(Step):
    """
    Formato del config de estandarizacion:
    {
        "source1":{
            "[nombre_columna1]": [
                {
                    "name":"[nombre_modulo]",
                    "config":{[config]}
                },
                ...
            }
        },
        "source2": idem
    }
    """

    def __init__(self, **kwargs):
        super(StandardizationStep, self).__init__(**kwargs)
        self.modules_directory = "standardization"

    @staticmethod
    def pretty_name():
        return "Standardization"

    def run_implementation(self):
        self._standardize_source(1)
        self._standardize_source(2)

    def _standardize_source(self, source_number):
        dal = DALMongo(self.project_id)
        records = dal.get_records(ExtractionStep().class_name, source_number)

        for record in records:
            for col, standardizations in self.config["source{}".format(source_number)].items():
                for standardization in standardizations:
                    module = self._load_module(standardization)
                    record.columns[col] = module.run(record.columns[col])

        self._append_result_collection(records, "source{}".format(source_number))

    def _load_module(self, standardization):
        step = self.modules_directory
        module = standardization['name']
        config = standardization['config']
        return dynamic_loading.load_module(step, module, config=config)


class SchemaMatchingStep(Step):
    """
    Formato del config de SchemaMatching:
    {
        "selected_module": {
            "name": "[nombre_modulo]",
            "config": {}
        }
    }
    """

    def __init__(self, **kwargs):
        super(SchemaMatchingStep, self).__init__(**kwargs)
        self.modules_directory = "schema-matching"

    @staticmethod
    def pretty_name():
        return "Schema matching"

    def run_implementation(self):
        module = self._load_module(project_id=self.project_id)

        self._append_result_collection(module.run())
