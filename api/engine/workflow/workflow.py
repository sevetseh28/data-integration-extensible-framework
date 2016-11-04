from engine.utils import dynamic_loading
from steps import *

FIRST_STEP = ExtractionStep

STEP_TABLE = {
    ExtractionStep: StandarizationStep
}


class Workflow:
    def __init__(self, project_id):
        self.step = None
        self.project_id = project_id

    def set_current_step(self, current_step, config):
        self.step = dynamic_loading.load_step(current_step, project_id=self.project_id, config=config)

    def execute_step(self):
        # se ejecuta el step
        self.step.run()

        # se avanza al siguiente step
        if type(self.step) in STEP_TABLE:
            result = STEP_TABLE[type(self.step)](None, None).class_name
        else:
            result = "no hay mas estados"

        return result
