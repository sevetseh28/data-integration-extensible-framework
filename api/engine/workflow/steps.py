# coding=utf-8
from __future__ import print_function
import logging
from abc import abstractmethod

from engine.dal_mongo import DALMongo
from engine.models.record import IndexingGroup, SimilarityVector, Column, Field
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

    def __init__(self, project_id=None, segmentation_skipped=False, config=None):
        self.results = {
            "collections": []
        }
        self.config = config
        self.class_name = type(self).__name__
        self.project_id = project_id
        self.segmentation_skipped = segmentation_skipped
        self.modules_directory = None

    def run(self):
        """
        Run generico. ejecuta cosas previas, ejecuta el step, y ejecuta cosas posteriores
        """
        logging.info("Starting step " + self.class_name)

        ret =self.run_implementation()

        # se guardan los resultados
        dal = DALMongo(self.project_id)
        dal.store_step_results(step=self.class_name, results=self.results)

        logging.info("Finished step " + self.class_name)
        return ret

    @abstractmethod
    def run_implementation(self):
        """
        Firma del run particular de cada step
        """
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def pretty_name():
        raise NotImplementedError

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

        # Make a list with columns specified by the user
        # used_cols = []
        # for col, datacleansing_modules in self.config["source{}".format(source_number)].items():
        #     if col not in used_cols:
        #         used_cols.append(col)
        #
        # all_cols = [col_obj.name for col_obj in dal.get_schema(source_number, 'ExtractionStep')]
        # extra_cols = [col for col in all_cols if col not in used_cols]

        #  Do cleansing for each column of each record
        for record in records:
            for col, datacleansing_modules in self.config["source{}".format(source_number)].items():
                for datacleansing_module in datacleansing_modules:
                    module = self._load_module(datacleansing_module)
                    #TODO the module should be given only the field value (string) and not the column
                    record.columns[col] = module.run(record.columns[col])

            # Remove extra columns
            # for extra_col in extra_cols:
            #     record.columns.pop(extra_col)

        self._append_result_collection(records, "source{}_records".format(source_number))

        #new_schema = [Column(c_name) for c_name in used_cols]
        #self._append_result_collection(new_schema, 'source{}_new_schema'.format(source_number))


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

        # Initialize columns to store new segmented schema
        orig_schema = {}
        for c_obj in dal.get_schema(source_number):
            orig_schema[c_obj.name] = c_obj

        new_cols = orig_schema

        # Run segmentation module for each column of each record
        for record in records:
            for col_name, segmentation_module in self.config["source{}".format(source_number)].items():
                module = self._load_module(segmentation_module)
                record.columns[col_name] = module.run(record.columns[col_name])

                # This is to create the new segmented schema
                for field_obj in record.columns[col_name].fields:
                    new_col_fields = new_cols[col_name].fields
                    # If a new output field was found in this column then add it to the new schema
                    if field_obj.output_field is not None and \
                        field_obj.output_field not in [field.output_field for field in new_col_fields]:
                        # TODO tags could be appended as well but for now we leave it empty
                        new_of = Field(value="n/A", tipe=field_obj.tipe, output_field=field_obj.output_field,
                                       tags=[])
                        new_cols[col_name].fields.append(new_of)

        # Reconstruct new_cols object so that the DAL can store it
        segmented_schema = []
        for col_name, col_obj in new_cols.items():
            segmented_schema.append(col_obj)

        self._append_result_collection(records, 'source{}_records'.format(source_number))
        self._append_result_collection(segmented_schema, 'source{}_schema'.format(source_number))

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
        if self.segmentation_skipped:
            dal.drop_segmentation()
            prevstep = "StandardisationAndTaggingStep"
        else:
            prevstep = "SegmentationStep"
        records1 = dal.get_records(prevstep, 1)
        records2 = dal.get_records(prevstep, 2)

        module = self._load_module(project_id=self.project_id, records1=records1, records2=records2)

        new_schema, records1, records2 = module.run()

        self._append_result_collection(records1, 'source1_records')
        self._append_result_collection(records2, 'source2_records')
        self._append_result_collection(new_schema, 'new_schema')


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

    # TODO comparison per output field per column
    {
        "[column1]":{
            "[output_field_1]":{
                "name":"[nombre_modulo]",
                "config":{[config]}
                "weight": <<float>>,
            },
            "[output_field_Wayfare_name]":{
                "name":"[nombre_modulo]",
                "config":{[config]}
                "weight": <<float>>,
            },
        },
        "[column2]":{
            "[output_field_Wayfare_name]":{
                "name":"[nombre_modulo]",
                "config":{[config]}
                "weight": <<float>>,
            },
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
        segmented_schema = dal.get_global_schema()
        output_fields_schema = {}
        matched_cols = []
        for column in segmented_schema:
            if column['name'].startswith("__new__"):
                output_fields_schema[column['name']] = column['fields']
                matched_cols.append(column['name'])
        simils = []

        max_weight = max([float(module['weight']) for idx, module in self.config.items()])

        for group in groups:
            for r1 in group.records1:
                for r2 in group.records2:
                    # Initialize similarity vector
                    sv = SimilarityVector(r1._id, r2._id, group=group.key)
                    for col in matched_cols: # could be r2.matched_cols() as well (they return the same)
                        if not self.segmentation_skipped:
                            for out_field, comparison_module in self.config.items():
                                # Check that the output field exists in the column, otherwise it wont create an entrance
                                # in the similarity vector
                                if out_field in [f['output_field'] for f  in output_fields_schema[col]]:
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
        module = self._load_module(project_id=self.project_id)

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
        },
        "only_matches": <boolean>
    }
    """

    def __init__(self, config, **kwargs):
        super(ExportStep, self).__init__(config=config, **kwargs)
        self.modules_directory = "export"
        self.only_matches = config['only_matches']

    @staticmethod
    def pretty_name():
        return "Export"

    def run_implementation(self):
        # Se obtienen los resultados del data fusion
        dal = DALMongo(self.project_id)

        records = dal.get_fused_records()

        if not self.only_matches:
            records += dal.get_non_matches()

        schema = dal.get_global_schema()

        return self._load_module(records=records, schema=schema).run()


