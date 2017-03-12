import json

from models import Project, StepConfig
from rest_framework import serializers


# ver http://www.django-rest-framework.org/tutorial/quickstart/#serializers

class StepConfigSerializer(serializers.HyperlinkedModelSerializer):
    config = serializers.SerializerMethodField()

    def get_config(self, obj):
        return dict(obj.config)#json.dumps(obj.config).encode('utf-8')

    class Meta:
        model = StepConfig


        fields = ('project', 'step', 'config')


class ProjectSerializer(serializers.ModelSerializer):
    steps = StepConfigSerializer(many=True, read_only=True)
    script = serializers.SerializerMethodField('has_script')

    def has_script(self,proj):
        return proj.steps.filter(step="ExportStep").count() > 0


    class Meta:
        model = Project
        fields = ('id', 'name', 'current_step', 'steps', 'script')
