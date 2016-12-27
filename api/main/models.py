from __future__ import unicode_literals

from django.db import models
from jsonfield import JSONField

from engine.workflow.steps import Step
from engine.workflow.workflow import FIRST_STEP

# Lista de steps con su represencacion para el campo step.
# https://docs.djangoproject.com/en/1.10/ref/models/fields/#django.db.models.Field.choices
STEPS = ((step.__name__, step.pretty_name()) for step in Step.__subclasses__())


class Project(models.Model):
    name = models.CharField(max_length=30)
    current_step = models.CharField(max_length=30, choices=STEPS, default=None, null=True)

    # Metodo para q se muestre con nombre para humanos en las apis navegables generadas
    def __str__(self):
        return self.name


class StepConfig(models.Model):
    project = models.ForeignKey(Project, related_name='steps')
    step = models.CharField(max_length=30, choices=STEPS)
    config = JSONField(True)

    def __str__(self):
        return self.project.__str__() + '.' + self.step
