import cv2
import numpy as np

def apply_yolo_object_detection(image_to_process, net, classes_to_look_for):
    layer_names = net.getLayerNames()
    out_layers_indexes = net.getUnconnectedOutLayers()
    out_layers = [layer_names[index - 1] for index in out_layers_indexes]

    with open("Resources/coco.names.txt") as file:
        classes = file.read().split("\n")

    height, width, _ = image_to_process.shape
    blob = cv2.dnn.blobFromImage(image_to_process, 1 / 255, (608, 608),
                                 (0, 0, 0), swapRB=True, crop=False)
    net.setInput(blob)
    outs = net.forward(out_layers)
    class_indexes, class_scores, boxes = ([] for i in range(3))

    # Starting a search for objects in an image
    for out in outs:
        for obj in out:
            scores = obj[5:]
            class_index = np.argmax(scores)
            class_score = scores[class_index]
            if class_score > 0:
                center_x = int(obj[0] * width)
                center_y = int(obj[1] * height)
                obj_width = int(obj[2] * width)
                obj_height = int(obj[3] * height)
                box = [center_x - obj_width // 2, center_y - obj_height // 2,
                       obj_width, obj_height]
                boxes.append(box)
                class_indexes.append(class_index)
                class_scores.append(float(class_score))

    # Selection
    chosen_boxes = cv2.dnn.NMSBoxes(boxes, class_scores, 0.0, 0.4)

    print(chosen_boxes)

    result = {}

    for look_class in classes_to_look_for:
        result[look_class] = 0

    for box_index in chosen_boxes:
        box_index = box_index
        box = boxes[box_index]
        class_index = class_indexes[box_index]

        print(classes[class_index], classes_to_look_for)

        # For debugging, we draw objects included in the desired classes
        current_class = classes[class_index]
        if current_class in classes_to_look_for:
            result[current_class] += 1

    print(result)

    return ''


def start_image_object_detection(img_path, classes_to_look_for):
    net = cv2.dnn.readNetFromDarknet("Resources/yolov4-tiny.cfg",
                                     "Resources/yolov4-tiny.weights")
    try:
        # Applying Object Recognition Techniques in an Image by YOLO
        image = cv2.imread(img_path)
        image = apply_yolo_object_detection(image, net, classes_to_look_for)

    except KeyboardInterrupt:
        pass


def detect_objects():
    # images_folder = glob.glob("video-images-opencv/*.png")

    image = "video-images-opencv/Пушкина/image0.png"
    look_for = "person,car"

    # Delete spaces
    list_look_for = look_for.split(',')

    classes_to_look_for = list_look_for

    start_image_object_detection(image, classes_to_look_for)
