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
            filter = {'$sample': {'size': limit}}
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

    def get_matches_info(self):
        """
        Retorna los matches de la clasificacion
        """
        results = self.get_all("ClassificationStep", with_id=True)

        ret = []
        count = [0, 0, 0]
        for r in results:
            if count[r['match_type']] == 5:
                continue
            new_r = {'record1': self._get_record_comparison_json(r['record1'], 1),
                     'record2': self._get_record_comparison_json(r['record2'], 2),
                     'match_type': r['match_type']}
            ret.append(new_r)
            count[r['match_type']] += 1
        return ret

    def _get_record_comparison_json(self, id, source_num):
        c = self.get_mongoclient()
        rec = c[self.db_name]['ComparisonStep'].find({'$or': [{'record1': id}, {'record2': id}]})[0]
        new_rec = []
        for c in rec['comparisons']:
            new_rec.append(c[source_num - 1])
        return new_rec

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

    @property
    def get_comparison_info(self, max_cant=20):
        """
        Returns compared data along with the similarity vector (in JSON format)
        :return:
        """
        n = max_cant
        # se agrupan las comparaciones por clave
        pipeline = [
            {'$sort': {'group': 1}},
            {
                '$group': {
                    '_id': '$group',
                    'comparisons': {'$push': '$$ROOT'},
                }
            }
        ]
        groups = self._get_aggregated('ComparisonStep', pipeline)

        groups = [g for g in groups]

        # se calcula el maximo de registros por grupo en base al n
        max_recs_per_group = n / len(groups) if len(groups) < n else 1

        # se carga el maximo de comparaciones por grupo agrupados por clave
        comparisons = {}
        for g in groups:
            for i in range(min(len(g['comparisons']), max_recs_per_group)):
                if g['_id'] not in comparisons:
                    comparisons[g['_id']] = []

                comparisons[g['_id']].append(g['comparisons'].pop())

        # el resultado anterior es agrupado por clave, aqui se aplana poniendo todos los registros juntos
        flattened = [item for k, sublist in comparisons.items() for item in sublist]

        # si todavia faltan registros, se completa con cualquiera de los restantes
        if len(flattened) < n:
            comps_left = n-len(flattened)

            for g in groups:
                for i in range(len(g['comparisons'])):
                    comparisons[g['_id']].append(g['comparisons'].pop())

                    #se lleva la cuenta de cuantos faltan para parar
                    comps_left -= 1
                    if comps_left == 0:
                        break
                if comps_left == 0:
                    break

        # se devuelve el array aplanado
        return [item for k, sublist in comparisons.items() for item in sublist]

    def get_total_comparisons_made(self):
        c = self.get_mongoclient()
        cursor = self.get_all('ComparisonStep', '')
        return cursor.count()

    def get_potential_matches_count(self):
        c = self.get_mongoclient()
        cursor = self.get_all('ClassificationStep', filters={'match_type': 2})
        return cursor.count()

    def get_non_matches_count(self):
        c = self.get_mongoclient()
        cursor = self.get_all('ClassificationStep', filters={'match_type': 0})
        return cursor.count()

    def get_matches_count(self):
        c = self.get_mongoclient()
        cursor = self.get_all('ClassificationStep', filters={'match_type': 1})
        return cursor.count()

    def get_extracted_data_count(self, source_number):
        c = self.get_mongoclient()
        cursor = self.get_all('ExtractionStep_source{}_records'.format(source_number))
        return cursor.count()

    def get_fused_preview(self):
        """
        Returns compared data along with the similarity vector (in JSON format)
        :return:
        """
        c = self.get_mongoclient()
        cursor = self.get_all('DataFusionStep', '')
        array_global_schema = self.get_global_schema()
        ret_info = []
        i = 0
        for rec in cursor:
            # r = {}
            #
            # for col in array_global_schema:
            #     for c in rec['columns']:
            #         if col['name'] == c['name']:
            #             if col['is_new']:
            #                 r[col['custom_name']] = {}
            #
            #                 for field in col['fields']:
            #                     for f in c['fields']:
            #                         if field['output_field'] == f['output_field']:
            #                             r[col['custom_name']][f['output_field']] = f['value']
            #             else:
            #                 r[col['name']] = ''
            #                 for f in c['fields']:
            #                     r[col['name']] += f['value']

            ret_info.append(rec)

        return ret_info

    def get_schema(self, source_number):  # , current_step):
        """
        Retorna el esquema original de una fuente

        :param source_number: numero de fuente (1 o 2)
        :return: columnas del esquema de la fuente
        """
        # If we are in a step after doing data cleansing then we have to retrieve the pruned cleansed schema.
        # if current_step == "ExtractionStep":
        #    schema = self.get_all("ExtractionStep", "source{}_schema".format(source_number))
        # else:
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
            if c['name'].startswith('__new__') and c['name'] not in [cl['name'] for cl in ret]:
                ret.append({'name': c['name'], 'custom_name': c['custom_name']})

        return ret

    def get_global_schema(self):
        """
        Retorna el esquema global luego de aplicado el schema matching
        """
        new_schema = self.get_all("SchemaMatchingStep", "new_schema")
        cols = [c for c in new_schema]

        return cols

    def get_limited_indexing_keys(self, limit):
        c = self.get_mongoclient()
        col = c[self.db_name]["IndexingStep"]

        # Se obtienen las keys de los grupos
        keys = []
        for k in col.aggregate([{"$group": {
            "_id": "$key",
            "count_s1": {"$sum": {
                "$cond": {"if": {"$eq": ["$source", 1]}, "then": 1, "else": 0}
            }},
            "count_s2": {"$sum": {
                "$cond": {"if": {"$eq": ["$source", 2]}, "then": 1, "else": 0}
            }}
        }}]):
            keys.append({'key': k['_id'], 'count_s1': k['count_s1'], 'count_s2': k['count_s2']})
            if len(keys) == limit:
                break
        return keys

    def get_count_indexing_groups(self):
        c = self.get_mongoclient()
        col = c[self.db_name]["IndexingStep"]

        # Se obtienen las keys de los grupos
        cursor = col.aggregate([{"$group": {
            "_id": "$key"
        }}])
        return len(list(cursor))

    def get_number_of_comparisons_to_do(self):
        c = self.get_mongoclient()
        col = c[self.db_name]["IndexingStep"]

        # Se obtienen las keys de los grupos
        result = col.aggregate([{"$group": {
            "_id": "$key",
            "count_s1": {"$sum": {
                "$cond": {"if": {"$eq": ["$source", 1]}, "then": 1, "else": 0}
            }},
            "count_s2": {"$sum": {
                "$cond": {"if": {"$eq": ["$source", 2]}, "then": 1, "else": 0}
            }}}},
            {"$group": {"_id": "$_id",
                        "comparisons": {"$sum": {"$multiply": ["$count_s1", "$count_s2"]}}
                        }},
            {"$group": {"_id": "all",
                        "total_comparisons": {"$sum": "$comparisons"}
                        }}])
        return result.next()['total_comparisons']

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

    def drop_segmentation(self):
        c = self.get_mongoclient()
        db = c[self.db_name]
        db['SegmentationStep_source1_records'].drop()
        db['SegmentationStep_source1_schema'].drop()
        db['SegmentationStep_source2_records'].drop()
        db['SegmentationStep_source2_schema'].drop()
        c.close()
