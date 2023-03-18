import json

from django.http import HttpResponse
from django.shortcuts import render

# from maps.services.FramesService import create_frames
from maps.services.MLService import counting_cars
from maps.services.OSMService import osm_query
from maps.services.VideoServices import create_map_video

import pandas as pd

SAVING_FRAMES_PER_SECOND = 1


tags = [
        {'highway': 'bus_stop'}, {'footway': 'crossing'},
        {'amenity': 'cafe'},
       ]

cities = ['Казань, Россия']


def index_view(request):
    context = {}
    return render(request, 'maps/index.html', context)


def create_video_view(request):
    create_map_video("Пушкина")
    return render(request, 'maps/index.html', {})


def counting_view(request):
    # create_frames()
    total_count = counting_cars()
    dict = {'count': total_count}
    return HttpResponse(json.dumps(dict), content_type='application/json')


def get_osm_data(request):
    gdfs = []
    for city in cities:
        for tag in tags:
            f = osm_query(tag, city)
            gdfs.append(f)

    data_poi = pd.concat(gdfs)
    print(data_poi.groupby(['city', 'object', 'type'], as_index=False).agg({'geometry': 'count'}))
    return render(request, 'maps/index.html', {})
