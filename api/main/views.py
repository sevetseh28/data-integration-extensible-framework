import json
import traceback
import uuid

from django.http import Http404
from django.http import JsonResponse
from django.http import HttpResponse
from rest_framework import viewsets

from engine import dal_mongo
from engine.utils.dynamic_loading import list_modules
from engine.workflow.workflow import Workflow
from serializers import *
import engine.dal_mongo


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
    # Rename step to match modules directory
    if step == 'datacleansing': step = 'data_cleansing'
    if step == 'standardisationtagging': step = 'standardisation_tagging'
    if step == 'schemamatching': step = 'schema_matching'
    if step == 'datafusion': step = 'data_fusion'
    return JsonResponse(list_modules(step, project_id), safe=False)


def schema(request, project_id):
    dal = dal_mongo.DALMongo(project_id)
    # project = Project.objects.get(id=project_id)

    schema1 = [c.name for c in dal.get_schema(1)]
    schema2 = [c.name for c in dal.get_schema(2)]

    return JsonResponse({
        'source1': schema1,
        'source2': schema2
    }, safe=False)


def segmentedschema(request, project_id):
    dal = dal_mongo.DALMongo(project_id)
    # project = Project.objects.get(id=project_id)

    schema1 = []
    schema2 = []
    for c in dal.get_segmented_schema(1):
        new_col = {'colname': c.name, 'segments': []}
        for segment in c.fields:
            new_col['segments'].append(segment.output_field)
        schema1.append(new_col)

    for c in dal.get_segmented_schema(2):
        new_col = {'colname': c.name, 'segments': []}
        for segment in c.fields:
            new_col['segments'].append(segment.output_field)
        schema2.append(new_col)

    return JsonResponse({
        'source1': schema1,
        'source2': schema2
    }, safe=False)


def globalschema(request, project_id):
    dal = dal_mongo.DALMongo(project_id)
    # project = Project.objects.get(id=project_id)
    schema = _transform_global_schema(dal.get_global_schema())
    return JsonResponse(schema, safe=False)


def _transform_global_schema(old_format_schema):
    schema = {'cant_cols': 0, 'schema': {}, 'segments': []}
    for c in old_format_schema:
        colname1 = c['name'].split('__')[2]
        colname2 = c['name'].split('__')[3]
        schema['schema'][colname1 + ' - ' + colname2] = []
        for field in c['fields']:
            schema['schema'][colname1 + ' - ' + colname2].append(field['output_field'])
            schema['segments'].append(field['output_field'])
            schema['cant_cols'] += 1
    return schema


def previewdata(request, project_id, step):
    dal = dal_mongo.DALMongo(project_id)

    previewdata1 = dal.get_aggregated_records(step, 1,
                                              pipeline=[{'$limit': 5}],
                                              json_format=True)

    previewdata2 = dal.get_aggregated_records(step, 2,
                                              pipeline=[{'$limit': 5}],
                                              json_format=True)

    new_previewdata1 = []
    new_previewdata2 = []

    for r in previewdata1:
        new_row = {}
        for col in r['columns']:
            new_row[col['name']] = col['fields']
        new_previewdata1.append(new_row)

    for r in previewdata2:
        new_row = {}
        for col in r['columns']:
            new_row[col['name']] = col['fields']
        new_previewdata2.append(new_row)

    return JsonResponse({
        'source1': new_previewdata1,
        'source2': new_previewdata2
    }, safe=False)


def comparisondata(request, project_id):
    dal = dal_mongo.DALMongo(project_id)
    data = dal.get_comparison_info()
    ret_data = []
    for d in data:
        new_d = {}
        new_d['vector'] = d['vector']
        new_d['comparisons'] = {'record1': [], 'record2': []}
        for c in d['comparisons']:
            new_d['comparisons']['record1'].append(c[0])
            new_d['comparisons']['record2'].append(c[1])
        ret_data.append(new_d)

    return JsonResponse(ret_data, safe=False)


def matchesresult(request, project_id):
    dal = dal_mongo.DALMongo(project_id)
    data = dal.get_matches_info()
    schema = _transform_global_schema(dal.get_global_schema())
    new_data = []
    for d in data:
        new_d = {'match_type': d['match_type'],
                 'record1': d['record1'],
                 'record2': d['record2']}
        new_data.append(new_d)
    return JsonResponse(new_data, safe=False)


def _transform_format_record(old_format_record):
    new_format_rec = {}
    for unsorted_col in old_format_record:
        new_format_rec[_get_colname_pretty(unsorted_col)] = []
        for field in unsorted_col['fields']:
            if field['value'] is None:
                pass
            new_format_rec[_get_colname_pretty(unsorted_col)].append(field['value'])


    # new_format_rec = []
    # for unsorted_col in old_format_record:
    #     for field in unsorted_col['fields']:
    #         new_format_rec.append(field['value'])
    new_format_rec_ordered = []
    for colname, vals in new_format_rec.iteritems():
        for val in vals:
            new_format_rec_ordered.append(val)
    return new_format_rec_ordered

def _get_colname_pretty(c):
    try:
        colname1 = c['name'].split('__')[2]
        colname2 = c['name'].split('__')[3]
    except:
        pass
    return colname1 + ' - ' + colname2

def upload(request):
    filename = uuid.uuid4()
    file = request.FILES['file']
    ext = file._name.split('.')[-1]

    with open('uploaded-files/{}.{}'.format(filename, ext), 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)

    return JsonResponse({'location': 'uploaded-files/{}.{}'.format(filename, ext)})


def download(request, filename, name):
    try:
        with open('files-to-download/{}'.format(filename), 'rb') as f:
            response = HttpResponse(f.read(), content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="{}.csv"'.format(name)
            return response
    except IOError as e:
        raise Http404
    except Exception as e:
        return JsonResponse({'status': 'error', 'details': e.message}, status=500)


def output_fields(request, project_id):
    """
    Method to return the output fields
    :param request:
    :param project_id:
    :return:
    """
    project = Project.objects.get(id=project_id)
    dal = dal_mongo.DALMongo(project_id)
    ret = {}
    if project.segmentation_skipped:
        ret['col_or_outputfield'] = "column"
        ret['values'] = dal.get_matched_cols()
    else:
        ret['col_or_outputfield'] = "output field"
        ret['values'] = dal.get_output_fields_matched_cols()

    return JsonResponse(ret, safe=False)


def run(request):
    """
    This is the run function for the current step.
    :param request: the request object
    :return: status json with ok message or error message.
    """
    try:
        # Se obtienen los parametros del request
        params = json.loads(request.body)
        project_id = params['project_id']
        step = params['step']
        config = params['config'] if 'config' in params else {}
        step_state = params['step_state'] if 'step_state' in params else {}
        project = Project.objects.get(id=project_id)
        # Se chequea si se skipea el paso de Segmentation
        downloadfile = False
        if step == "SegmentationStep":
            project.segmentation_skipped = config['skipstep']
            if not project.segmentation_skipped:
                # Llamado a workflow
                w = Workflow(project_id, project.segmentation_skipped)
                w.set_current_step(step, config)
                w.execute_step()
        else:
            # Llamado a workflow
            w = Workflow(project_id, project.segmentation_skipped)
            w.set_current_step(step, config)

            if step == "ExportStep":
                downloadfile = w.execute_step()
            else:
                w.execute_step()

        # se guarda el estado del proyecto
        project.current_step = step
        project.save()

        saved_step, created = StepConfig.objects.get_or_create(project_id=project_id, step=step)
        saved_step.config = step_state
        saved_step.save()
    except Exception as e:
        # DEBUG PURPOSES
        print(traceback.format_exc())
        # return JsonResponse({'status': 'error', 'details': traceback.format_exc()}, status=500)

        # TODO Should be in the final version instead
        return JsonResponse({'status': 'error', 'details': e.message}, status=500)

    if not downloadfile:
        return JsonResponse({'status': 'ok'})
    else:
        return JsonResponse({'status': 'ok', 'downloadfile': {'name': downloadfile[0], 'filename': downloadfile[1]}})
