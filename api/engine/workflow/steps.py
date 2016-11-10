# coding=utf-8
from __future__ import print_function
import logging
from abc import abstractmethod

from engine.dal_mongo import DALMongo
from engine.models.record import IndexingGroup, SimilarityVector
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

    def run_implementation(self):
        """
        Firma del run particular de cada step
        Implementación por defecto
        """
        module = self._load_module(project_id=self.project_id)

        self._append_result_collection(module.run())

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
        # Se obtienen los registros
        dal = DALMongo(self.project_id)
        records = dal.get_records(ExtractionStep().class_name, source_number)

        # Se aplican las estandarizaciones para cada columna de cada registro
        for record in records:
            for col, standardizations in self.config["source{}".format(source_number)].items():
                for standardization in standardizations:
                    module = self._load_module(standardization)
                    record.columns[col] = module.run(record.columns[col])

        self._append_result_collection(records, "source{}_records".format(source_number))

    def _load_module(self, standardization):
        step = self.modules_directory
        module = standardization['name']
        config = standardization['config']
        return dynamic_loading.load_module(step, module, config=config)


class SegmentationStep(Step):
    """
    Formato del config de Segmentation:
    {
        "selected_module": {
            "name": "[nombre_modulo]",
            "config": {}
        }
    }
    """

    def __init__(self, **kwargs):
        super(SegmentationStep, self).__init__(**kwargs)
        self.modules_directory = "segmentation"

    @staticmethod
    def pretty_name():
        return "Segmentation"

    def run_implementation(self):
        self._segment_source(1)
        self._segment_source(2)

    def _segment_source(self, source_number):
        dal = DALMongo(self.project_id)

        records = dal.get_records(StandardizationStep().class_name, source_number)
        module = self._load_module(records=records)

        self._append_result_collection(module.run(), 'source{}_records'.format(source_number))


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


class IndexingStep(Step):
    """
    Formato del config de IndexingStep:
    {
        "selected_module": {
            "name": "[nombre_modulo]",
            "config": {
            }
        }
    }
    """

    def __init__(self, **kwargs):
        super(IndexingStep, self).__init__(**kwargs)
        self.modules_directory = "indexing"

    @staticmethod
    def pretty_name():
        return "Indexing"

    def run_implementation(self):
        groups1 = self._get_groups(1)
        groups2 = self._get_groups(2)

        result_groups = []

        for k, group1 in groups1.items():
            groups1.pop(k)
            group2 = groups2.pop(k, None)

            if group2:
                result_groups.append(IndexingGroup(k, group1, group2))

        self._append_result_collection(result_groups)

    def _get_groups(self, source_number):
        dal = DALMongo(self.project_id)

        records = dal.get_records(SegmentationStep().class_name, source_number)
        module = self._load_module(records=records)
        return module.run()


class ComparisonStep(Step):
    """
    Compara los valores de los fields que tienen el mismo output field dentro de los grupos de columnas matcheadas
    en la etapa de schema matching.

    Formato del config de comparacion:
    {
        "[output_field]":{
            "name":"[nombre_modulo]",
            "config":{[config]}
        },
        ...
    }
    """

    def __init__(self, **kwargs):
        super(ComparisonStep, self).__init__(**kwargs)
        self.modules_directory = "comparison"

    @staticmethod
    def pretty_name():
        return "Comparison"

    def run_implementation(self):
        # Se obtienen los grupos de registros

        dal = DALMongo(self.project_id)

        groups = dal.get_indexing_groups()
        schmatches = dal.get_schema_matching()

        simils = []

        for group in groups:
            for r1 in group.records1:
                for r2 in group.records2:
                    # Inicializa el vector de comparacion vacio
                    sv = SimilarityVector(r1._id, r2._id)

                    for schmatch in schmatches.schema_matches:
                        # Inicializa la comparacion con 0
                        sv.vector.append(0)

                        for out_field, comparison in self.config.items():
                            # Se obienen los valores a comparar y se comparan
                            out_field_value1 = r1.get_output_field_cols(out_field, schmatch['source1'])
                            out_field_value2 = r2.get_output_field_cols(out_field, schmatch['source2'])

                            module = self._load_module(comparison)

                            # Actualiza el valor de la comparacion en el vector
                            sv.vector[-1] = module.run(out_field_value1, out_field_value2)

                    simils.append(sv)

        self._append_result_collection(simils)

    def _load_module(self, comparison):
        step = self.modules_directory
        module = comparison['name']
        config = comparison['config']
        return dynamic_loading.load_module(step, module, config=config)


class ClassificationStep(Step):
    """
        Define cuales de los pares dados por el paso de comparacion corresponden a matches

        Formato del config de clasificación:
        {
            "selected_module":{
                "name":"[nombre_modulo]",
                "config":{[config]}
            }
        }
    """

    def __init__(self, **kwargs):
        super(ClassificationStep, self).__init__(**kwargs)
        self.modules_directory = "classification"

    @staticmethod
    def pretty_name():
        return "Classification"

    def run_implementation(self):
        # Se obtienen los vectores de similitud
        dal = DALMongo(self.project_id)

        simils = dal.get_similarity_vectors()

        match_results = []
        module = self._load_module()

        for simil in simils:
            match_results.append(module.run(simil))

        self._append_result_collection(match_results)
