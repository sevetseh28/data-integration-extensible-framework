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

    def __init__(self, project_id=None,segment_skipped=False, config=None):
        self.results = {
            "collections": []
        }
        self.config = config
        self.class_name = type(self).__name__
        self.project_id = project_id
        self.segment_skipped = segment_skipped
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
        Firma del run particular de cada step
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


class DataCleansingStep(Step):
    """
    Formato del config de Data cleansing:
    {
        "source1":{
            "[column_name1]": [
                {
                    "name":"[module_name]",
                    "config":{[config]}
                },
                ...
            }
        },
        "source2": same as above
    }
    """

    def __init__(self, **kwargs):
        super(DataCleansingStep, self).__init__(**kwargs)
        self.modules_directory = "data_cleansing"

    @staticmethod
    def pretty_name():
        return "Data Cleansing"

    def run_implementation(self):
        self._clean_source(1)
        self._clean_source(2)

    def _clean_source(self, source_number):
        # Se obtienen los registros
        dal = DALMongo(self.project_id)
        records = dal.get_records(ExtractionStep().class_name, source_number)

        #  Do cleaning for each column of each record
        for record in records:
            for col, datacleansing_modules in self.config["source{}".format(source_number)].items():
                for datacleansing_module in datacleansing_modules:
                    module = self._load_module(datacleansing_module)
                    record.columns[col] = module.run(record.columns[col])

        self._append_result_collection(records, "source{}_records".format(source_number))

    def _load_module(self, datacleansing):
        step = self.modules_directory
        module = datacleansing['name']
        config = datacleansing['config']
        return dynamic_loading.load_module(step, module, config=config)

class StandardisationAndTaggingStep(Step):
    """
    Config format for standardisation and tagging step:
    {
        "source1":{
            "[column_name1]":
                {
                    "name":"[module_name]",
                    "config":{[config]}
                }
            }
            "[column_name2]":
                {
                    "name":"[module_name]",
                    "config":{[config]}
                }
            },
            ...
        },
        "source2": idem
    }
    """

    def __init__(self, **kwargs):
        super(StandardisationAndTaggingStep, self).__init__(**kwargs)
        self.modules_directory = "standardisation_tagging"

    @staticmethod
    def pretty_name():
        return "Standardisation & Tagging"

    def run_implementation(self):
        self._standardise_and_tag_source(1)
        self._standardise_and_tag_source(2)

    def _standardise_and_tag_source(self, source_number):
        # Get cleansed records from MongoDB
        dal = DALMongo(self.project_id)
        records = dal.get_records(DataCleansingStep().class_name, source_number)

        # Run standardisation and tagging module for each column of each record
        for record in records:
            for col, standardisation_tagging_module in self.config["source{}".format(source_number)].items():
                module = self._load_module(standardisation_tagging_module)
                record.columns[col] = module.run(record.columns[col])

        self._append_result_collection(records, "source{}_records".format(source_number))

    def _load_module(self, standardisation_tagging_module):
        step = self.modules_directory
        module = standardisation_tagging_module['name']
        config = standardisation_tagging_module['config']
        return dynamic_loading.load_module(step, module, config=config)


class SegmentationStep(Step):
    """
    Config format for segmentation step:
    {
        "source1":{
            "[column_name1]":
                {
                    "name":"[module_name]",
                    "config":{[config]}
                }
            }
            "[column_name2]":
                {
                    "name":"[module_name]",
                    "config":{[config]}
                }
            },
            ...
        },
        "source2": idem
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

        records = dal.get_records(StandardisationAndTaggingStep().class_name, source_number)
        # module = self._load_module(records=records)

        # Run segmentation module for each column of each record
        for record in records:
            for col, segmentation_module in self.config["source{}".format(source_number)].items():
                module = self._load_module(segmentation_module)
                record.columns[col] = module.run(record.columns[col])

        self._append_result_collection(records, 'source{}_records'.format(source_number))

    def _load_module(self, segmentation_module):
        step = self.modules_directory
        module = segmentation_module['name']
        config = segmentation_module['config']
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
        self.modules_directory = "schema_matching"

    @staticmethod
    def pretty_name():
        return "Schema matching"

    def run_implementation(self):
        """
        Firma del run particular de cada step
        Implementación por defecto
        """
        dal = DALMongo(self.project_id)
        if self.segment_skipped:
            prevstep = "StandardisationAndTaggingStep"
        else:
            prevstep = "SegmentationStep"
        records1 = dal.get_records(prevstep, 1)
        records2 = dal.get_records(prevstep, 2)

        module = self._load_module(project_id=self.project_id, records1=records1, records2=records2)

        records1, records2 = module.run()

        self._append_result_collection(records1, 'source1_records')
        self._append_result_collection(records2, 'source2_records')


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

        records = dal.get_records(SchemaMatchingStep().class_name, source_number)
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
            "weight": <<float>>,
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

        simils = []

        max_weight = max([float(module['weight']) for idx, module in self.config.items()])

        for group in groups:
            for r1 in group.records1:
                for r2 in group.records2:
                    # Inicializa el vector de comparacion vacio
                    sv = SimilarityVector(r1._id, r2._id)
                    for col in r1.matched_cols(): # could be r2.matched_cols() as well (they return the same)
                        if not self.segment_skipped:
                            for out_field, comparison_module in self.config.items():
                                # Se obienen los valores a comparar y se comparan
                                out_field_value1 = r1.get_output_field_col(out_field,col)
                                out_field_value2 = r2.get_output_field_col(out_field,col)

                                module = self._load_module(comparison_module)

                                weight = float(comparison_module['weight'])

                                # Actualiza el valor de la comparacion en el vector
                                sim_value = module.run(out_field_value1, out_field_value2)
                                sim_value_weighted = sim_value * weight / max_weight
                                sv.vector.append(sim_value_weighted)
                                sv.comparisons.append([out_field_value1, out_field_value2])
                        else:
                            comparison_module = self.config[col]

                            # Se obienen los valores completos de la columna
                            column_value_s1 = r1.get_field_col(col)
                            column_value_s2 = r2.get_field_col(col)

                            module = self._load_module(comparison_module)

                            weight = float(comparison_module['weight'])

                            # Actualiza el valor de la comparacion en el vector
                            sim_value = module.run(column_value_s1, column_value_s2)
                            sim_value_weighted = sim_value * weight / max_weight
                            sv.vector.append(sim_value_weighted)
                            sv.comparisons.append([column_value_s1, column_value_s2])
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


class DataFusionStep(Step):
    """
        Fusiona los matches

        Formato del config de clasificación:
        {
            "selected_module":{
                "name":"[nombre_modulo]",
                "config":{[config]}
            }
        }
    """

    def __init__(self, **kwargs):
        super(DataFusionStep, self).__init__(**kwargs)
        self.modules_directory = "data_fusion"

    @staticmethod
    def pretty_name():
        return "Data fusion"

    def run_implementation(self):
        # Se obtienen los resultados de la comparación
        dal = DALMongo(self.project_id)

        matches = dal.get_matches()

        module = self._load_module(project_id=self.project_id, matches=matches)
        fused_records = module.run()

        self._append_result_collection(fused_records)


class ExportStep(Step):
    """
    Formato del config de exportacion:
    {
        "selected_module": {
            "name":"[un_nombre]",
            "config":{[config]}
        }
    }
    """

    def __init__(self, **kwargs):
        super(ExportStep, self).__init__(**kwargs)
        self.modules_directory = "export"

    @staticmethod
    def pretty_name():
        return "Export"

    def run_implementation(self):
        # Se obtienen los resultados del data fusion
        dal = DALMongo(self.project_id)

        records = dal.get_fused_records()
        records += dal.get_non_matches()

        self._load_module(records=records).run()

