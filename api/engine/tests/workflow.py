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
    "schema-matching1": {
        "selected_module": {
            "name": "dummy",
            "config": {}
        }
    },
    "schema-matching2": {
        "selected_module": {
            "name": "manual",
            "config": {
                'matches': [
                    {
                        'source1': [
                            'Column1',
                            'Column2'
                        ],
                        'source2': [
                            'Column2',
                            'Column4'
                        ]
                    }
                ]
            }
        }
    },
    "standardization": {
        "source1": {
            "Column1": [
                {
                    "name": "lowercase",
                    "config": {}
                },
                {
                    "name": "delete-chars",
                    "config": {"chars": "_"}
                }
            ],
        },
        "source2": {
            "Column1": [
                {
                    "name": "delete-chars",
                    "config": {"chars": "_"}
                },
                {
                    "name": "lowercase",
                    "config": {}
                }

            ],
        }
    },
    "indexing1": {
        "selected_module": {
            "name": "blocking-standard",
            "config": {"keys": ["Column1", "Column2"]}
        }
    },
    "indexing2": {
        "selected_module": {
            "name": "full",
            "config": {}
        }
    }
}

dal = DALMongo(project_id)
dal.drop_database()

w.set_current_step("ExtractionStep", config["extraction"])
w.execute_step()

w.set_current_step("StandardizationStep", config["standardization"])
w.execute_step()

w.set_current_step("SchemaMatchingStep", config["schema-matching1"])
w.execute_step()

w.set_current_step("SchemaMatchingStep", config["schema-matching2"])
w.execute_step()

w.set_current_step("IndexingStep", config["indexing1"])
w.execute_step()

w.set_current_step("IndexingStep", config["indexing2"])
w.execute_step()
