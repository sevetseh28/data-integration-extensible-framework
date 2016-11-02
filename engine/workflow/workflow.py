from steps import *

first_step = ExtractionStep

step_table = {
    ExtractionStep: StandarizationStep
}



class Workflow:
    def __init__(self):
        self.step = first_step()

    def execute_step(self, config = None):
        self.step.run(config)
        if type(self.step) in step_table:
            self.step = step_table[type(self.step)]()
        else:
            print("no hay mas estados")
