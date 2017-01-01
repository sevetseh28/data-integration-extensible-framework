from engine.utils import dynamic_loading
from steps import *

FIRST_STEP = ExtractionStep


class Workflow:
    def __init__(self, project_id,segment_skipped):
        self.step = None
        self.project_id = project_id
        self.segment_skipped = segment_skipped

    def set_current_step(self, current_step, config):
        self.step = dynamic_loading.load_step(current_step, project_id=self.project_id, segment_skipped = self.segment_skipped, config=config)

    def execute_step(self):
        # se ejecuta el step
        return self.step.run()
