import subprocess
import os
import glob

from playwright.sync_api import sync_playwright

from maps.services.DadataService import get_address_by_coord

MAPS_URL = 'http://127.0.0.1:8000/maps/'
VIDEO_RECORD_DIR = 'videos/'

os.environ["IMAGEIO_FFMPEG_EXE"] = "/usr/bin/ffmpeg"


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
        page.wait_for_timeout(1000)
        for i in range(30):
            page.keyboard.press('ArrowUp')
            page.keyboard.press('ArrowUp')

            x = page.get_by_test_id('coordinate-x').all_inner_texts()[0]
            y = page.get_by_test_id('coordinate-y').all_inner_texts()[0]

            address = get_address_by_coord(x, y)
            page.screenshot(path='video-images-opencv/image' + str(i) + '.png')
            page.wait_for_timeout(500)
        browser.close()
        context.close()


def create_map_video():
    record_video_with_playwright()
    # convert_webm_to_mp4()


