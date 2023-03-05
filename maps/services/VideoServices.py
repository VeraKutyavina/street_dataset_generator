import subprocess
import os
import glob

from playwright.sync_api import sync_playwright

MAPS_URL = 'http://127.0.0.1:8000/maps/'
VIDEO_RECORD_DIR = 'videos/'


def convert_webm_to_mp4():
    list_of_files = glob.glob(VIDEO_RECORD_DIR + '*')
    input_file = max(list_of_files, key=os.path.getctime)
    output_file = 'videos/data-record.mp4'
    command = 'ffmpeg -i ' + input_file + ' ' + output_file
    subprocess.run(command, shell=True)


def record_video_with_playwright():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context(record_video_dir=VIDEO_RECORD_DIR)
        page = context.new_page()
        page.goto(MAPS_URL)
        page.wait_for_timeout(2000)

        for i in range(25):
            page.locator('canvas').click(position={'x': 614, 'y': 478}, timeout=15000)
            page.wait_for_timeout(500)
        browser.close()
        context.close()
        convert_webm_to_mp4()


def create_map_video():
    record_video_with_playwright()


