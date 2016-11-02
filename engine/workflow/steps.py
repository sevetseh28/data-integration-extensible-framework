from __future__ import print_function


class Step:
    def __init__(self):
        pass

    def run(self, config):
        print("run " + config)


class ExtractionStep(object, Step):
    def __init__(self):
        super(ExtractionStep, self).__init__()

    def run(self, config):
        super(ExtractionStep, self).run("ExtractionStep")


class StandarizationStep(object, Step):
    def __init__(self):
        super(StandarizationStep, self).__init__()

    def run(self, config):
        super(StandarizationStep, self).run("StandarizationStep")
