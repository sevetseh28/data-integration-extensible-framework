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
            # Si la coleccion es vacia, pasa a la siguiente
            if not collection['values']:
                continue

            # Se obtiene la coleccion (si no existe se crea)
            collection_name = self._col_from_step_and_suffix(step, collection['name_suffix'])
            real_collection = db[collection_name]

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

    def get_records(self, step, source_number):
        """
        Retorna los records de una fuente para un step

        :param step: nombre de la clase del step
        :param source_number: numero de fuente (1 o 2)
        :return: registros de la fuente resultado de ejecutar el step
        """
        records = self.get_all(step, "source{}_records".format(source_number))

        return [Record.from_json(r) for r in records]

    def get_schema(self, source_number):
        """
        Retorna el esquema original de una fuente

        :param source_number: numero de fuente (1 o 2)
        :return: columnas del esquema de la fuente
        """
        schema = self.get_all("ExtractionStep", "source{}_schema".format(source_number))

        return [Column.from_json(c) for c in schema]

    def get_all(self, step, suffix):
        """
        Retorna una coleccion dado el step y suffix

        :param step: nombre de la clase del step
        :param suffix: sufijo de la coleccion
        :return: documentos de la coleccion de ese step con ese sufijo
        """
        return self._get_all(self._col_from_step_and_suffix(step, suffix))

    def _get_all(self, collection_name):
        """
        Retorna toda una coleccion

        :param collection_name: nombre de coleccion
        :return: documentos de la coleccion
        """
        c = self.get_connection()

        col = c[self.db_name][collection_name]
        result = col.find({}, {'_id': False})

        c.close()
        return result

    """""""""""""""""""""""""""""""""""""""""""""""""""
        UTILS
    """""""""""""""""""""""""""""""""""""""""""""""""""

    def _col_from_step_and_suffix(self, step, suffix):
        if suffix:
            return "{}_{}".format(step, suffix)
        return step

    def drop_database(self):
        c = self.get_connection()
        c.drop_database(self.db_name)
