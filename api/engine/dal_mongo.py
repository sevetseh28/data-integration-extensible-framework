from json import dumps

from pymongo import MongoClient
from django.conf import settings

from api.api.settings import DATABASES


def get_connection():
    host = DATABASES['mongodb']['host']
    port = DATABASES['mongodb']['port']
    return MongoClient(host, port)


def store_step_results(project_id, step, results):
    c = get_connection()

    db = c['project' + str(project_id)]

    for collection in results['collections']:
        # Se obtiene la coleccion (si no existe se crea)
        real_collection = db[step + collection['name']]

        # Se pasan a Json los records
        json_values = [r.to_json() for r in collection['values']]

        real_collection.insert_many(json_values)
