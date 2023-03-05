import json

from django.http import HttpResponse
from django.shortcuts import render
from playwright.sync_api import sync_playwright
from vehicle_detector import VehicleDetector

from datetime import timedelta
import cv2
import numpy as np
import subprocess
import os
import glob
os.environ["IMAGEIO_FFMPEG_EXE"] = "/usr/bin/ffmpeg"

SAVING_FRAMES_PER_SECOND = 1


def index(request):
    context = {}
    return render(request, 'maps/index.html', context)


def convert_webm_mp4_subprocess():
    list_of_files = glob.glob('videos/*')
    input_file = max(list_of_files, key=os.path.getctime)
    output_file = 'videos/data-record.mp4'
    command = 'ffmpeg -i ' + input_file + ' ' + output_file
    subprocess.run(command, shell=True)


# create video with maps
def create_video(request):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context(record_video_dir="videos/")
        page = context.new_page()
        page.goto('http://127.0.0.1:8000/maps/')
        page.wait_for_timeout(2000)

        for i in range(25):
            print(i)
            page.locator('canvas').click(position={'x': 614, 'y': 478}, timeout=15000)
            page.wait_for_timeout(500)
        print(page.title())
        browser.close()
        context.close()
        convert_webm_mp4_subprocess()
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


def webp_mp4(request):
    convert_webm_mp4_subprocess()
    return render(request, 'maps/index.html', {})


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
