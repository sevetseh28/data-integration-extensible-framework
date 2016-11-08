from django.http import JsonResponse

from engine.utils.dynamic_loading import list_modules
from rest_framework import viewsets
from serializers import *


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all().order_by('name')
    serializer_class = ProjectSerializer


class StepConfigViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = StepConfig.objects.all()
    serializer_class = StepConfigSerializer


def available_modules(request, step='', project_id=None):
    return JsonResponse(list_modules(step, project_id), safe=False)

