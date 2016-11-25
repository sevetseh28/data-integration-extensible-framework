from django.http import JsonResponse

from engine.utils.dynamic_loading import list_modules
from rest_framework import viewsets

from engine.workflow.workflow import Workflow
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

def run(request):
    # Se obtienen los parametros del request
    project_id = request.POST['project_id']
    step = request.POST['step']
    config = request.POST['config']

    # Llamado a workflow
    w = Workflow(project_id)
    w.set_current_step(step, config)
    w.execute_step()

    return JsonResponse(list_modules(step, project_id), safe=False)

