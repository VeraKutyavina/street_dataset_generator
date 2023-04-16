import cv2
import numpy as np

lower_red = np.array([0, 70, 50])
upper_red = np.array([10, 255, 255])
lower_blue = np.array([110, 50, 50])
upper_blue = np.array([130, 255, 255])
lower_green = np.array([50, 50, 50])
upper_green = np.array([70, 255, 255])
lower_black = np.array([0, 0, 0])
upper_black = np.array([180, 255, 30])
lower_white = np.array([0, 0, 200])
upper_white = np.array([180, 30, 255])


def save_img(box, image_to_process, i):
    x, y, w, h = box
    cropped_image = image_to_process[y:y + h, x:x + w]
    cv2.imwrite(f'box_{i}.jpg', cropped_image)
    i += 1


def detect_colors(img, boxes):
    # преобразование в цветовое пространство HSV
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # пороговая обработка для выделения машин каждого цвета
    mask_red = cv2.inRange(hsv, lower_red, upper_red)
    mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)
    mask_green = cv2.inRange(hsv, lower_green, upper_green)
    mask_white = cv2.inRange(hsv, lower_green, upper_green)
    mask_black = cv2.inRange(hsv, lower_green, upper_green)

    # находим цвет
    for contour in boxes:
        x, y, w, h = contour

        blue_score = cv2.mean(mask_blue[y:y + h, x:x + w])[0]
        white_score = cv2.mean(mask_white[y:y + h, x:x + w])[0]
        black_score = cv2.mean(mask_black[y:y + h, x:x + w])[0]
        red_score = cv2.mean(mask_red[y:y + h, x:x + w])[0]
        green_score = cv2.mean(mask_green[y:y + h, x:x + w])[0]

        scores = {'blue': blue_score, 'white': white_score, 'black': black_score, 'red': red_score, 'green': green_score}
        color = max(scores, key=scores.get)

        print(color)


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

    i = 0
    for box in chosen_boxes:
        save_img(boxes[box], image_to_process, i)
        i += 1

    result = {}
    cars_boxes = []

    for look_class in classes_to_look_for:
        result[look_class] = 0

    for box_index in chosen_boxes:
        class_index = class_indexes[box_index]

        current_class = classes[class_index]
        if current_class in classes_to_look_for:
            result[current_class] += 1

        if current_class == 'car':
            cars_boxes.append(boxes[box_index])

    print(result)

    detect_colors(image_to_process, cars_boxes)

    # i = 0
    # img = cv2.cvtColor(image_to_process, cv2.COLOR_BGR2RGB)
    # img = torch.from_numpy(img).permute(2, 0, 1).float().unsqueeze(0) / 255.0
    # for box_item in boxes:
    #     x1, y1, x2, y2 = box_item
    #     cv2.rectangle(img, (int(x1), int(y1)), (int(x2), int(y2)), (255, 0, 0), 2)
    #     cropped_img = img[:, :, int(y1):int(y2), int(x1):int(x2)]
    #
    #     # Сохранение вырезанной части изображения с помощью OpenCV
    #     cv2.imwrite(f'result_{i}.jpg', cropped_img.permute(1, 2, 0).numpy() * 255)
    #     i += 1

    return ''


def start_image_object_detection(img_path, classes_to_look_for):
    net = cv2.dnn.readNetFromDarknet("Resources/yolov4-tiny.cfg",
                                     "Resources/yolov4-tiny.weights")
    try:
        image = cv2.imread(img_path)
        apply_yolo_object_detection(image, net, classes_to_look_for)

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
