from engine.dal_mongo import DALMongo
from engine.models.record import *
from engine.modules.module import Module


class DummySchemaMatching(Module):
    """
    Matchea las columnas de los 2 esquemas 1 a 1 desde comienzo al final del que tenga menos columnas
    """

    def __init__(self, project_id, **kwargs):
        super(DummySchemaMatching, self).__init__(**kwargs)
        self.project_id = project_id

    def run(self):
        match = SchemaMatch()

        dal = DALMongo(self.project_id)

        schema1 = dal.get_schema(1)
        schema2 = dal.get_schema(2)

        for i in range(min(len(schema1), len(schema2))):
            match.add_match([schema1[i]], [schema2[i]])

        return match
