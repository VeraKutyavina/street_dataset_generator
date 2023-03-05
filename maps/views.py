import json

from django.http import HttpResponse
from django.shortcuts import render

from maps.services.OSMService import osm_query
from maps.classes.vehicle_detector import VehicleDetector
from maps.services.VideoServices import create_map_video

import pandas as pd
from datetime import timedelta
import cv2
import numpy as np
import os
import glob


# os.environ["IMAGEIO_FFMPEG_EXE"] = "/usr/bin/ffmpeg"

SAVING_FRAMES_PER_SECOND = 1


tags = [
        {'highway': 'bus_stop'}, {'footway': 'crossing'},
        {'amenity': 'cafe'},
       ]

cities = ['Казань, Россия']


def index(request):
    context = {}
    return render(request, 'maps/index.html', context)


def create_video(request):
    create_map_video()
    return render(request, 'maps/index.html', {})


def format_timedelta(td):
    result = str(td)
    try:
        result, ms = result.split(".")
    except ValueError:
        return result + ".00".replace(":", "-")
    ms = int(ms)
    ms = round(ms / 1e4)
    return f"{result}.{ms:02}".replace(":", "-")


def get_saving_frames_durations(cap, saving_fps):
    s = []
    print(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    print(cap.get(cv2.CAP_PROP_FPS))
    clip_duration = cap.get(cv2.CAP_PROP_FRAME_COUNT) / cap.get(cv2.CAP_PROP_FPS)
    for i in np.arange(0, clip_duration, 1 / saving_fps):
        s.append(i)
    return s


def create_frames():
    video_file = 'videos/data-record.mp4'
    filename = 'video-images'
    filename += "-opencv"
    if not os.path.isdir(filename):
        os.mkdir(filename)
    cap = cv2.VideoCapture(video_file)
    fps = cap.get(cv2.CAP_PROP_FPS)
    saving_frames_per_second = min(fps, SAVING_FRAMES_PER_SECOND)
    saving_frames_durations = get_saving_frames_durations(cap, saving_frames_per_second)
    count = 0
    while True:
        is_read, frame = cap.read()
        if not is_read:
            break
        frame_duration = count / fps
        try:
            closest_duration = saving_frames_durations[0]
        except IndexError:
            break
        if frame_duration >= closest_duration:
            frame_duration_formatted = format_timedelta(timedelta(seconds=frame_duration))
            cv2.imwrite(os.path.join(filename, f"frame{frame_duration_formatted}.jpg"), frame)
            try:
                saving_frames_durations.pop(0)
            except IndexError:
                pass
        count += 1


def counting(request):
    create_frames()
    vd = VehicleDetector()
    images_folder = glob.glob("video-images-opencv/*.jpg")
    vehicles_folder_count = 0

    for img_path in images_folder:
        print("Img path", img_path)
        img = cv2.imread(img_path)
        vehicle_boxes = vd.detect_vehicles(img)
        vehicle_count = len(vehicle_boxes)
        vehicles_folder_count += vehicle_count

    dict = {'count': vehicles_folder_count}

    print("Total count", vehicles_folder_count)

    return HttpResponse(json.dumps(dict), content_type='application/json')


def get_osm_data(request):
    gdfs = []
    for city in cities:
        for tag in tags:
            f = osm_query(tag, city)
            gdfs.append(f)

    data_poi = pd.concat(gdfs)
    print(data_poi.groupby(['city', 'object', 'type'], as_index=False).agg({'geometry': 'count'}))
