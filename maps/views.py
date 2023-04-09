import json
import time

from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader

from maps.forms import CreateDatasetForm
from maps.healpers import collect_screenshots
from maps.services.MLService import counting_cars
from maps.services.OSMService import get_street_data

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
    total_count = counting_cars()
    dict = {'count': total_count}
    return HttpResponse(json.dumps(dict), content_type='application/json')


def get_osm_data(request):
    get_street_data('Казань')
    return render(request, 'maps/index.html', {})
