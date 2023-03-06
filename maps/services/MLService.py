from maps.classes.vehicle_detector import VehicleDetector
import cv2
import glob


def counting_cars():
    vd = VehicleDetector()
    images_folder = glob.glob("video-images-opencv/*.jpg")
    vehicles_folder_count = 0

    for img_path in images_folder:
        print("Img path", img_path)
        img = cv2.imread(img_path)
        vehicle_boxes = vd.detect_vehicles(img)
        vehicle_count = len(vehicle_boxes)
        vehicles_folder_count += vehicle_count

    print("Total count", vehicles_folder_count)

    return vehicles_folder_count
