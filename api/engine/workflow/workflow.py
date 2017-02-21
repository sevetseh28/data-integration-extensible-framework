from engine.utils import dynamic_loading
from steps import *

FIRST_STEP = ExtractionStep


class Workflow:
    def __init__(self, project_id, segmentation_skipped):
        self.step = None
        self.project_id = project_id
        self.segmentation_skipped = segmentation_skipped

    def set_current_step(self, current_step, config):
        self.step = dynamic_loading.load_step(current_step,
                                              project_id=self.project_id,
                                              segmentation_skipped=self.segmentation_skipped,
                                              config=config)

    def execute_step(self):
        return self.step.run()
