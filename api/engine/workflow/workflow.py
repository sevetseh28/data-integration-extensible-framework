from engine.utils import dynamic_loading
from steps import *

FIRST_STEP = ExtractionStep

STEP_TABLE = {
    ExtractionStep: StandardisationAndTaggingStep
}


class Workflow:
    def __init__(self, project_id):
        self.step = None
        self.project_id = project_id

    def set_current_step(self, current_step, config):
        self.step = dynamic_loading.load_step(current_step, project_id=self.project_id, config=config)

    def execute_step(self):
        # se ejecuta el step
        return self.step.run()
