from django.conf import settings
from engine.workflow.workflow import Workflow

settings.configure()
w = Workflow(0)

config = {
    "source1": {
        "selected_module": {
            "name":"dummy",
            "config":{}
        }
    },
    "source2": {
        "selected_module": {
            "name":"dummy",
            "config":{}
        }
    }
}
w.set_current_step("ExtractionStep", config)

w.execute_step()