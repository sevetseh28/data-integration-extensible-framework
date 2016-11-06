from models import Project, StepConfig
from rest_framework import serializers


# ver http://www.django-rest-framework.org/tutorial/quickstart/#serializers

class ProjectSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Project
        fields = ('name', 'stepconfig_set')


class StepConfigSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = StepConfig
        fields = ('project', 'step', 'config')
