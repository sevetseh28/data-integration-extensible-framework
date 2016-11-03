# coding=utf-8
from __future__ import print_function


class Step(object):
    def __init__(self):
        pass

    def run(self, config):
        print("run " + config)


class ExtractionStep(Step):
    def __init__(self):
        super(ExtractionStep, self).__init__()

    @staticmethod
    def pretty_name():
        return "Extracción"

    def run(self, config):
        super(ExtractionStep, self).run("ExtractionStep")


class StandarizationStep(Step):
    def __init__(self):
        super(StandarizationStep, self).__init__()

    @staticmethod
    def pretty_name():
        return "Estandarización"

    def run(self, config):
        super(StandarizationStep, self).run("StandarizationStep")
