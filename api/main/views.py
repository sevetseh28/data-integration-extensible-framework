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

def finalschema(request, project_id):
    dal = dal_mongo.DALMongo(project_id)
    # project = Project.objects.get(id=project_id)
    schema = _transform_final_schema(dal.get_global_schema())
    return JsonResponse(schema, safe=False)


def _transform_global_schema(old_format_schema):
    schema = {'cant_cols': 0, 'schema': [], 'segments': []}
    for c in old_format_schema:
        if c['is_new']:
            col = {
                'name': c['custom_name'],
                'fields': []
            }
            for field in c['fields']:
                col['fields'].append(field['output_field'])
                schema['segments'].append(field['output_field'])
                schema['cant_cols'] += 1

            schema['schema'].append(col)

    return schema

def _transform_final_schema(old_format_schema):
    schema = {'cant_cols': 0, 'schema': [], 'segments': []}
    for c in old_format_schema:
        new_s = {}
        schema['schema'].append(new_s)
        col_name = c['custom_name'] or c['name']
        new_s[col_name] = []
        for field in c['fields']:
            new_s[c['custom_name']].append(field['output_field'])
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
        'source1': {'results': new_previewdata1, 'total_count': dal.get_extracted_data_count(1)},
        'source2': {'results': new_previewdata2, 'total_count': dal.get_extracted_data_count(2)}
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

    response = {'results': ret_data, 'total_comparisons_made': dal.get_total_comparisons_made()}
    return JsonResponse(response, safe=False)

def fuseddata(request, project_id):
    dal = dal_mongo.DALMongo(project_id)
    data = dal.get_fused_preview()
    return JsonResponse(data, safe=False)


def matchesresult(request, project_id):
    dal = dal_mongo.DALMongo(project_id)
    data = dal.get_matches_info()
    schema = _transform_global_schema(dal.get_global_schema())
    matches = []
    non_matches = []
    potential_matches = []
    for d in data:
        new_d = {'match_type': d['match_type'],
                 'record1': d['record1'],
                 'record2': d['record2']}
        if d['match_type'] == 0:
            non_matches.append(new_d)
        elif d['match_type'] == 1:
            matches.append(new_d)
        elif d['match_type'] == 2:
            potential_matches.append(new_d)

    response = {
        'results': matches + potential_matches + non_matches,
        'total_data': dal.get_total_comparisons_made(),
        'total_matches': dal.get_matches_count(),
        'total_potential_matches': dal.get_potential_matches_count(),
        'total_non_matches': dal.get_non_matches_count()
    }
    return JsonResponse(response, safe=False)


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

def indexingdata(request, project_id):
    project = Project.objects.get(id=project_id)
    dal = dal_mongo.DALMongo(project_id)
    return JsonResponse({'results': dal.get_limited_indexing_keys(25),
                         'cant_idx_groups': dal.get_count_indexing_groups(),
                         'cant_comparisons': dal.get_number_of_comparisons_to_do(),
                         'cant_comparisons_full_index': dal.get_extracted_data_count(1) * dal.get_extracted_data_count(2)},
                        safe=False)

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
        if 'step_state' in params:
            step_state = params['step_state']
            saved_step, created = StepConfig.objects.get_or_create(project_id=project_id, step=step)
            saved_step.config = step_state
            saved_step.script_data = config
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

def get_script(request,project_id):
    if StepConfig.objects.filter(project_id = project_id, step="ExportStep").count() > 0:
        list_steps = ["Extraction Step", "Data Cleansing Step",
                      "Standardisation And Tagging Step", "Segmentation Step", "Schema Matching Step",
                      "Indexing Step", "Comparison Step","Classification Step","Data Fusion Step", "Export Step"]
        httphost = request.META["HTTP_HOST"]
        response = HttpResponse(content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename="script.py"'
        script = ""
        script += 'import urllib2\nimport json\nhost = "%s"\nproject_id = %s\n' %(httphost,project_id)
        for stepname in list_steps:
            try:
                step = StepConfig.objects.get(project_id= project_id,step=stepname.replace(" ",""))
                script += 'print "Executing %s..."\n' % stepname
                script += "config = json.loads(r'''"
                script += json.dumps(step.script_data)
                script += "''')"
                script += "\n"
                script += 'data = {"project_id": project_id,"step": "%s", "config": config }\n' % stepname.replace(" ","")
                script += 'req = urllib2.Request("http://%s/run/" % host)\nreq.add_header("Content-Type", "application/json")\nresponse = urllib2.urlopen(req, json.dumps(data))\n'
                if stepname != "Export Step":
                    script += "print response.read()\n"
                else:
                    script += 'stringjson = response.read()\ndictjson = json.loads(stringjson)\n' \
                              'if "downloadfile" in dictjson:\n\tname = dictjson["downloadfile"]["name"]\n\t' \
                              'filename = dictjson["downloadfile"]["filename"]\n\tprint "Download file in http://%s/download-file/%s/%s" % (host,filename, name)\n' \
                              'else:\n\tprint stringjson\n'
                script +="\n"
            except Exception as e:
                response.write("Error in %s configuration" %stepname)
                return response

        response.write(script)
        return response

