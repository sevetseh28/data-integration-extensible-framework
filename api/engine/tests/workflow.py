from django.conf import settings

from engine.dal_mongo import DALMongo
from engine.workflow.workflow import Workflow

settings.configure()
project_id = 0
w = Workflow(project_id)

config = {
    "extraction": {
        "source1": {
            "selected_module": {
                "name": "dummy",
                "config": {}
            }
        },
        "source2": {
            "selected_module": {
                "name": "dummy",
                "config": {}
            }
        }
    },
    "schema-matching": {
        "selected_module": {
            "name": "dummy",
            "config": {}
        }
    },
    "standardization": {
        "source1": {
            "Column1": [
                {
                    "name": "lowercase",
                    "config": {}
                },
            ],
        },
        "source2": {
            "Column1": [
                {
                    "name": "delete-chars",
                    "config": {"chars": "_"}
                },
            ],
        }
    }
}

dal = DALMongo(project_id)
dal.drop_database()
w.set_current_step("ExtractionStep", config["extraction"])
w.execute_step()

w.set_current_step("StandardizationStep", config["standardization"])
w.execute_step()

w.set_current_step("SchemaMatchingStep", config["schema-matching"])
w.execute_step()
