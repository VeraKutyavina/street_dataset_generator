import subprocess
import os
import glob

from playwright.sync_api import sync_playwright

from maps.services.AddreessService import get_heading_param
from maps.services.DadataService import get_address_by_coord
from maps.services.OSMService import get_random_points
from maps.services.TomTomService import get_street_name
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


def record_video_with_playwright(coordinates, street, heading, screens_addresses_dict, points):
    i = 0
    url = MAPS_URL + '?x=' + str(coordinates[1]) + '&y=' + str(coordinates[0]) + '&heading=' + str(heading)
    points.append([float(coordinates[1]), float(coordinates[0])])
    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context(record_video_dir=VIDEO_RECORD_DIR)
        page = context.new_page()
        page.goto(url)
        page.wait_for_timeout(1000)
        current_address = [street]
        current_x = '1'
        current_y = '1'
        k = 0
        while any(street in addr for addr in current_address):
            page.keyboard.press('ArrowUp')
            page.keyboard.press('ArrowUp')

            x = page.get_by_test_id('coordinate-x').all_inner_texts()[0]
            y = page.get_by_test_id('coordinate-y').all_inner_texts()[0]

            if x == current_x and y == current_y:
                points.append([float(x), float(y)])
                break
            else:
                current_x = x
                current_y = y

            print("Current points: (" + str(x) + "," + str(y) + ")")

            if not x == '' and not y == '':
                current_address = get_address_by_coord(x, y)
                # print(current_address)

            path_name = 'video-images-opencv/' + street + '/image' + str(i) + '.png'
            screens_addresses_dict[path_name] = current_address[0]

            page.screenshot(path=path_name)
            i += 1
            page.wait_for_timeout(500)
            k += 1
            if k == 10:
                points.append([float(x), float(y)])
                k = 0
        browser.close()
        context.close()

    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context(record_video_dir=VIDEO_RECORD_DIR)
        page = context.new_page()
        page.goto(url)
        page.wait_for_timeout(1000)
        current_address = [street]
        while any(street in addr for addr in current_address):
            page.keyboard.press('ArrowDown')
            page.keyboard.press('ArrowDown')

            x = page.get_by_test_id('coordinate-x').all_inner_texts()[0]
            y = page.get_by_test_id('coordinate-y').all_inner_texts()[0]

            if x == current_x and y == current_y:
                break
            else:
                current_x = x
                current_y = y

            print("Current points for second step: (" + str(x) + "," + str(y) + ")")
            if not x == '' and not y == '':
                current_address = get_address_by_coord(x, y)
                print(current_address)

            path_name = 'video-images-opencv/' + street + '/image' + str(i) + '.png'
            page.screenshot(path=path_name)
            screens_addresses_dict[path_name] = current_address[0] + ":" + x + ", " + y
            i += 1
            page.wait_for_timeout(500)
        browser.close()
        context.close()


def create_map_video(address, screens_addresses_dict, points_new):
    coordinates = get_coord_by_address(address)
    street = get_street_name(coordinates[1], coordinates[0])
    points = get_random_points(address)
    heading = get_heading_param(points[0], points[1])

    record_video_with_playwright(coordinates, street, heading, screens_addresses_dict, points_new)
