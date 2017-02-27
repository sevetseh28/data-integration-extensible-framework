# coding=utf-8
from json import dumps

from pymongo import MongoClient
from django.conf import settings

from api.settings import DATABASES
from engine.models.record import *

COL_STEP_PREFIXES = {
    "extraction": "ExtractionStep",

}


class DALMongo:
    def __init__(self, project_id=None):
        self.db_name = 'project{}'.format(project_id)
        self.mongoclient = MongoClient(DATABASES['mongodb']['host'], DATABASES['mongodb']['port'])

    def get_mongoclient(self):
        return self.mongoclient

    """""""""""""""""""""""""""""""""""""""""""""""""""
        INSERTS
    """""""""""""""""""""""""""""""""""""""""""""""""""

    def store_step_results(self, results, step):
        c = self.get_mongoclient()

        db = c[self.db_name]

        for collection in results['collections']:
            # Se obtiene la coleccion (si no existe se crea)
            collection_name = self._col_from_step_and_suffix(step, collection['name_suffix'])
            real_collection = db[collection_name]

            # Se vacia la coleccion (por si se esta re-ejecutando el step)
            db[collection_name].drop()

            # Si la coleccion es vacia, pasa a la siguiente
            if not collection['values']:
                db.create_collection(collection_name)
                continue

            # Se pasan a Json los valores
            # Si es iterable se convierte cada elemento
            if hasattr(collection['values'], '__iter__'):
                if step == "IndexingStep":
                    json_values = [v for v in collection['values'] for v in v.to_json()]
                else:
                    json_values = [v.to_json() for v in collection['values']]
            else:
                json_values = collection['values'].to_json()

            real_collection.insert_many(json_values)

        c.close()

    """""""""""""""""""""""""""""""""""""""""""""""""""
        GETS
    """""""""""""""""""""""""""""""""""""""""""""""""""
    def get_aggregated_records(self, step, source_number, pipeline, json_format=True):
        records = self.get_aggregated(step, "source{}_records".format(source_number), with_id=False, pipeline=pipeline)

        if not json_format:
            return [Record.from_json(r) for r in records]
        else:
            return [r for r in records]

    def get_records(self, step, source_number, limit=None, json_format=False):
        """
        Retorna los records de una fuente para un step

        :param step: nombre de la clase del step
        :param source_number: numero de fuente (1 o 2)
        :return: registros de la fuente resultado de ejecutar el step
        """
        filter = None
        if limit:
            filter = { '$sample': { 'size': limit } }
        records = self.get_all(step, "source{}_records".format(source_number), with_id=True, filters=filter)

        if not json_format:
            return [Record.from_json(r) for r in records]
        else:
            for r in records:
                r.pop('_id', None)
            return records

    def get_fused_records(self):
        """
        Retorna los records finales
        """
        records = self.get_all("DataFusionStep")

        return [Record.from_json(r) for r in records]

    def get_match_pair(self, match):
        """
        Retorna el par de registros de un match
        """

        r1 = self.get_all("SchemaMatchingStep", "source1_records", filters={"_id": match.record1}).next()
        r2 = self.get_all("SchemaMatchingStep", "source2_records", filters={"_id": match.record2}).next()

        return Record.from_json(r1), Record.from_json(r2)

    def get_matches(self):
        """
        Retorna los matches de la clasificacion
        """
        results = self.get_all("ClassificationStep", filters={"match_type": 1}, with_id=True)

        return [MatchResult.from_json(r) for r in results]

    def get_non_matches(self):
        """
        Retorna los no-matches de la clasificacion
        """
        results = self.get_all("ClassificationStep", filters={"match_type": 1}, with_id=True)
        results = [r for r in results]

        s1_ids = [r["record1"] for r in results]
        s2_ids = [r["record2"] for r in results]

        nonmatches1 = self.get_all("SchemaMatchingStep", "source1_records", filters={"_id": {"$nin": s1_ids}},
                                   with_id=True)
        nonmatches2 = self.get_all("SchemaMatchingStep", "source2_records", filters={"_id": {"$nin": s2_ids}},
                                   with_id=True)

        return [Record.from_json(r) for r in nonmatches1] + [Record.from_json(r) for r in nonmatches2]

    # def get_classification_results(self):
    #     """
    #     Retorna los resultados de la clasificación
    #     """
    #     results = self.get_all("ClassificationStep")
    #
    #     return [MatchResult.from_json(r) for r in results]

    def get_similarity_vectors(self):
        """
        Retorna los vectores de similaridad dados por el paso de comparacion
        """
        svs = self.get_all("ComparisonStep")

        return [SimilarityVector.from_json(sv) for sv in svs]

    def get_indexing_groups(self):
        """
        Retorna los grupos dados por el paso de indexacion
        :return: Lista de IndexingGroup
        """
        c = self.get_mongoclient()
        col = c[self.db_name]["IndexingStep"]

        # Se obtienen las keys de los grupos
        keys = [k["_id"] for k in col.aggregate([{"$group": {"_id": "$key"}}])]

        groups = []
        for key in keys:
            group_source1 = [Record.from_json(r) for r in col.find({"key": key, "source": 1})]
            group_source2 = [Record.from_json(r) for r in col.find({"key": key, "source": 2})]

            group = IndexingGroup(key, group_source1, group_source2)

            groups.append(group)

        c.close()

        return groups

    def get_schema(self, source_number): #, current_step):
        """
        Retorna el esquema original de una fuente

        :param source_number: numero de fuente (1 o 2)
        :return: columnas del esquema de la fuente
        """
        # If we are in a step after doing data cleansing then we have to retrieve the pruned cleansed schema.
        #if current_step == "ExtractionStep":
        #    schema = self.get_all("ExtractionStep", "source{}_schema".format(source_number))
        #else:
        #    schema = self.get_all("DataCleansingStep", "source{}_new_schema".format(source_number))
        schema = self.get_all("ExtractionStep", "source{}_schema".format(source_number))


        return [Column.from_json(c) for c in schema]

    def get_segmented_schema(self, source_number):
        """
        Returns a list with the output fields name for the given column name. It there are no output fields then
        returns an empty list
        :param column_name:
        :return:
        """
        mongoclient = self.get_mongoclient()

        db = mongoclient[self.db_name]
        segschema = self.get_all("SegmentationStep", "source{}_schema".format(source_number))

        return [Column.from_json(c) for c in segschema]



    def get_output_fields_matched_cols(self):
        """
        Returns the output fields of matched columns`
        """
        records = self.get_all("SchemaMatchingStep", "new_schema")
        ret = []

        for c in records:
            if c['name'].startswith('__new__'):
                for f in c['fields']:
                    if f['output_field'] not in [of['name'] for of in ret]:
                        ret.append({'name': f['output_field']})
        return ret

    def get_matched_cols(self):
        """
        Returns the matched columns
        """
        cols = self.get_all("SchemaMatchingStep", "new_schema")
        ret = []

        for c in cols:
            if c['name'] not in [cl['name'] for cl in ret]:
                ret.append({'name': c['name'], 'custom_name': c['custom_name']})

        return ret

    def get_global_schema(self):
        """
        Retorna el esquema global luego de aplicado el schema matching
        """
        new_schema = self.get_all("SchemaMatchingStep", "new_schema")
        cols = [c for c in new_schema]

        return cols

    # def get_schema_matching(self):
    #     """
    #     Retorna el esquema matching
    #     """
    #     schema = self.get_all("SchemaMatchingStep", "")
    #     json = [match for match in schema]
    #
    #     return SchemaMatch.from_json(json)

    def get_all(self, step, suffix="", with_id=False, filters=None):
        """
        Retorna una coleccion dado el step y suffix

        :param step: nombre de la clase del step
        :param suffix: sufijo de la coleccion
        :return: documentos de la coleccion de ese step con ese sufijo
        """
        return self._get_all(self._col_from_step_and_suffix(step, suffix), with_id, filters)

    def _get_all(self, collection_name, with_id=False, filters=None):
        """
        Retorna toda una coleccion

        :param collection_name: nombre de coleccion
        :return: documentos de la coleccion
        """
        if filters is None:
            filters = {}
        c = self.get_mongoclient()

        extra = {'_id': False}
        if with_id:
            extra = None

        col = c[self.db_name][collection_name]
        result = col.find(filters, extra)

        # c.close()
        return result

    def get_aggregated(self, step, suffix="", with_id=False, pipeline=None):
        """
        Retorna una coleccion dado el step y suffix

        :param step: nombre de la clase del step
        :param suffix: sufijo de la coleccion
        :return: documentos de la coleccion de ese step con ese sufijo
        """
        return self._get_aggregated(self._col_from_step_and_suffix(step, suffix), pipeline)

    def _get_aggregated(self, collection_name, pipeline=None):
        """
        Retorna toda una coleccion

        :param collection_name: nombre de coleccion
        :return: documentos de la coleccion
        """
        c = self.get_mongoclient()

        col = c[self.db_name][collection_name]
        result = col.aggregate(pipeline)

        # c.close()
        return result
    """""""""""""""""""""""""""""""""""""""""""""""""""
        UTILS
    """""""""""""""""""""""""""""""""""""""""""""""""""

    def _col_from_step_and_suffix(self, step, suffix):
        if suffix:
            return "{}_{}".format(step, suffix)
        return step

    def drop_database(self):
        c = self.get_mongoclient()
        c.drop_database(self.db_name)
        c.close()
