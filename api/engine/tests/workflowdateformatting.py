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
                "name": "csv-extractor",
                "config": {
            'pathcsv': "testdateformatting.csv"
        }
            }
        },
        "source2": {
            "selected_module": {
                "name": "dummy",
                "config": {}
            }
        }
    },
    "standardization": {
        "source1": {
            "FECHA": [
                {
                    "name": "date-formatting",
                    "config": {"languages":["en"]}
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
    "segmentation": {
        "selected_module": {
            "name": "nop",
            "config": {}
        }
    },
    "schema-matching": {
        "selected_module": {
            "name": "manual",
            "config": {
                'matches': [
                    {
                        'source1': [
                            'TARCONX'
                        ],
                        'source2': [
                            'Column2',
                            'Column4'
                        ]
                    },
                    {
                        'source1': [
                            'TRALOC'
                        ],
                        'source2': [
                            'Column4'
                        ]
                    }
                ]
            }
        }
    },
    "indexing1": {
        "selected_module": {
            "name": "blocking-standard",
            "config": {"keys": ["s1_TRCURR", "s1_TROPN1"]}
        }
    },
    "indexing2": {
        "selected_module": {
            "name": "full",
            "config": {}
        }
    },
    "comparison": {
        "": {
            "name": "equals",
            "config": {}
        }
    },
    "classification": {
        "selected_module": {
            "name": "fellegi-sunter",
            "config": {
                "thresholds":{
                    "from": 0.3,
                    "to": 0.5
                },
                "vector_reducer": 'average'
            }
        }
    },
    "data-fusion": {
        "selected_module": {
            "name": "preferred-source",
            "config": {
                "preferred-source": 1
            }
        }
    },
    "export": {
        "selected_module": {
            "name": "mongodb",
            "config": {
                'host': "localhost",
                'port': 27017,
                'db': "base",
                'collection': "coso"
            }
        }
    }
}

dal = DALMongo(project_id)
dal.drop_database()

w.set_current_step("ExtractionStep", config["extraction"])
w.execute_step()

w.set_current_step("StandardizationStep", config["standardization"])
w.execute_step()

w.set_current_step("SegmentationStep", config["segmentation"])
w.execute_step()

w.set_current_step("SchemaMatchingStep", config["schema-matching"])
w.execute_step()

w.set_current_step("IndexingStep", config["indexing1"])
w.execute_step()

w.set_current_step("IndexingStep", config["indexing2"])
w.execute_step()

w.set_current_step("ComparisonStep", config["comparison"])
w.execute_step()

w.set_current_step("ClassificationStep", config["classification"])
w.execute_step()

w.set_current_step("DataFusionStep", config["data-fusion"])
w.execute_step()

w.set_current_step("ExportStep", config["export"])
w.execute_step()
