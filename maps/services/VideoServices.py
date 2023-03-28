import subprocess
import os
import glob

from playwright.sync_api import sync_playwright

from maps.services.DadataService import get_address_by_coord, get_street_by_coord
from maps.services.YandexService import get_coord_by_address

MAPS_URL = 'http://127.0.0.1:8000/maps/'
VIDEO_RECORD_DIR = 'videos/'

os.environ["IMAGEIO_FFMPEG_EXE"] = "/usr/bin/ffmpeg"


def convert_webm_to_mp4():
    list_of_files = glob.glob(VIDEO_RECORD_DIR + '*')
    input_file = max(list_of_files, key=os.path.getctime)
    output_file = 'videos/data-record.mp4'
    command = 'ffmpeg -i ' + input_file + ' ' + output_file
    subprocess.run(command, shell=True)


def record_video_with_playwright(coordinates, address):
    i = 0
    url = MAPS_URL + '?x=' + str(coordinates[1]) + '&y=' + str(coordinates[0])
    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context(record_video_dir=VIDEO_RECORD_DIR)
        page = context.new_page()
        page.goto(url)
        page.wait_for_timeout(1000)
        current_address = [address]
        while any(address in x for x in current_address):
            page.keyboard.press('ArrowUp')
            page.keyboard.press('ArrowUp')

            x = page.get_by_test_id('coordinate-x').all_inner_texts()[0]
            y = page.get_by_test_id('coordinate-y').all_inner_texts()[0]

            if not x == '' and not y == '':
                current_address = get_address_by_coord(x, y)
                print(current_address)
            page.screenshot(path='video-images-opencv/image' + str(i) + '.png')
            i += 1
            page.wait_for_timeout(500)
        browser.close()
        context.close()

    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context(record_video_dir=VIDEO_RECORD_DIR)
        page = context.new_page()
        page.goto(url)
        page.wait_for_timeout(1000)
        current_address = [address]
        while any(address in x for x in current_address):
            page.keyboard.press('ArrowDown')
            page.keyboard.press('ArrowDown')

            x = page.get_by_test_id('coordinate-x').all_inner_texts()[0]
            y = page.get_by_test_id('coordinate-y').all_inner_texts()[0]

            if not x == '' and not y == '':
                current_address = get_address_by_coord(x, y)
                print("second")
                print(current_address)
            page.screenshot(path='video-images-opencv/image' + str(i) + '.png')
            i += 1
            page.wait_for_timeout(500)
        browser.close()
        context.close()


def create_map_video(address):
    coordinates = get_coord_by_address(address)
    street = get_street_by_coord(coordinates[1], coordinates[0])
    record_video_with_playwright(coordinates, street)
    # convert_webm_to_mp4()


