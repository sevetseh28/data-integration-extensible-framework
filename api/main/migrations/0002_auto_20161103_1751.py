# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-03 20:51
from __future__ import unicode_literals

from django.db import migrations, models
import engine.workflow.steps


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='current_step',
            field=models.CharField(choices=[(b'ExtractionStep', b'Extracci\xc3\xb3n'), (b'StandarizationStep', b'Estandarizaci\xc3\xb3n')], default=engine.workflow.steps.ExtractionStep, max_length=30),
        ),
        migrations.AlterField(
            model_name='stepconfig',
            name='step',
            field=models.CharField(max_length=30),
        ),
    ]
