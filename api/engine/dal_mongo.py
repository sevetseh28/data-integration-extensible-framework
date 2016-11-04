from json import dumps

from pymongo import MongoClient
from django.conf import settings

from api.api.settings import DATABASES
from api.engine.models.record import *

COL_STEP_PREFIXES = {
    "extraction": "ExtractionStep",

}


class DALMongo:
    def __init__(self, project_id=None):
        self.db_name = 'project{}'.format(project_id)

    def get_connection(self):
        host = DATABASES['mongodb']['host']
        port = DATABASES['mongodb']['port']
        return MongoClient(host, port)

    """""""""""""""""""""""""""""""""""""""""""""""""""
        INSERTS
    """""""""""""""""""""""""""""""""""""""""""""""""""

    def store_step_results(self, results, step):
        c = self.get_connection()

        db = c[self.db_name]

        for collection in results['collections']:
            # Se obtiene la coleccion (si no existe se crea)
            collection_name = self._col_from_step_and_suffix(step, collection['name_suffix'])
            real_collection = db[collection_name]

            # Se pasan a Json los valores
            # Si es iterable se convierte cada elemento
            if hasattr(collection['values'], '__iter__'):
                json_values = [v.to_json() for v in collection['values']]
            else:
                json_values = collection['values'].to_json()

            real_collection.insert_many(json_values)

        c.close()

    """""""""""""""""""""""""""""""""""""""""""""""""""
        GETS
    """""""""""""""""""""""""""""""""""""""""""""""""""

    # Retorna el esquema original de una fuente
    def get_schema(self, source_number):
        schema = self.get_all("ExtractionStep", "source{}_schema".format(source_number))

        return [Column.from_json(c) for c in schema]

    # Retorna una coleccion dado el step y suffix
    def get_all(self, step, suffix):
        return self._get_all(self._col_from_step_and_suffix(step, suffix))

    # Retorna toda la coleccion
    def _get_all(self, collection_name):
        c = self.get_connection()

        col = c[self.db_name][collection_name]
        result = col.find({})

        c.close()
        return result

    """""""""""""""""""""""""""""""""""""""""""""""""""
        UTILS
    """""""""""""""""""""""""""""""""""""""""""""""""""

    # def _db_from_project(self):
    #     return 'project' + self.project_id


    def _col_from_step_and_suffix(self, step, suffix):
        if suffix:
            return "{}_{}".format(step, suffix)
        return step
