import json
import os
import time

from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader

from maps.forms import CreateDatasetForm
from maps.healpers import collect_screenshots

SAVING_FRAMES_PER_SECOND = 1


tags = [
        {'highway': 'bus_stop'}, {'footway': 'crossing'},
        {'amenity': 'cafe'},
       ]

cities = ['Казань, Россия']


def index_view(request):
    context = {}
    return render(request, 'maps/index.html', context)


def user_form_view(request):
    template = loader.get_template('maps/user_form.html')
    context = {'form': CreateDatasetForm()}
    return HttpResponse(template.render(context, request))


def create_video_view(request):
    start_time = time.time()

    if request.method == 'POST':
        collect_screenshots(request)

    total = time.time() - start_time

    print('Total time: ' + str(total))

    dict = {}
    return HttpResponse(json.dumps(dict), content_type='application/json')


def counting_view(request):
    dict = {'count': 0}
    return HttpResponse(json.dumps(dict), content_type='application/json')


def get_osm_data(request):
    # if request.method == 'POST':
    #     collect_osm_data(request)
    return render(request, 'maps/index.html', {})


def download_file(request):
    file_path = 'data.json'
    with open(file_path, 'rb') as fh:
        response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
        response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
        return response
