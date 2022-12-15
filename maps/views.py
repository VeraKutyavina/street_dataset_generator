from django.shortcuts import render
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny

from maps.serializer import ScreenshotCreateSerializer
from playwright.sync_api import sync_playwright

from datetime import timedelta
import cv2
import numpy as np
import subprocess
import os
os.environ["IMAGEIO_FFMPEG_EXE"] = "/usr/bin/ffmpeg"

SAVING_FRAMES_PER_SECOND = 1


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


def index(request):
    context = {}
    return render(request, 'maps/index.html', context)


# create video with maps
def test(request):
    print('wehdbjwhebd')
    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context(record_video_dir="videos/")
        page = context.new_page()
        page.goto('http://127.0.0.1:8000/maps/')
        page.wait_for_timeout(5000)

        for i in range(50):
            print("рас ", i)
            page.locator('canvas').click(position={'x': 614, 'y': 478}, timeout=15000)
            page.wait_for_timeout(1000)
        page.locator('wedhbjhwebdjhbwejdhbjhwbe').click()
        print(page.title())
        browser.close()
        context.close()
    return render(request, 'maps/index.html', {})

def create_frames(request):
    video_file = 'videos/test.mp4'
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
    return render(request, 'maps/index.html', {})


def convert_webm_mp4_subprocess():
    input_file = 'videos/822f744fb2a54023b072d18f42684d26.webm'
    output_file = 'videos/test.mp4'
    command = 'ffmpeg -i ' + input_file + ' ' + output_file
    subprocess.run(command, shell=True)


def webp_mp4(request):
    convert_webm_mp4_subprocess()
    return render(request, 'maps/index.html', {})


def counting(request):
    return render(request, 'maps/index.html', {})

class SaveScreenshot(CreateAPIView):
    serializer_class = ScreenshotCreateSerializer
    permission_classes = [AllowAny]
