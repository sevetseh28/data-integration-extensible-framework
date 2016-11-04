from django.conf import settings
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
}

w.set_current_step("ExtractionStep", config["extraction"])
w.execute_step()

w.set_current_step("SchemaMatchingStep", config["schema-matching"])
w.execute_step()
