import os
import onnxruntime as ort
import numpy as np
import time
import cv2
from PIL import Image, ImageDraw, ImageFont

import config
from model.OrderInfo import OrderInfo


params = {
    'conf_thres': 0.5,  # 置信度阈值
    'iou_thres': 0.4,   # 非极大值抑制（NMS）的IoU阈值
}

classes = {
    0: "肉块",
    1: "小刀",
    2: "土豆(切)"
}
colors = np.random.uniform(0, 255, size=(len(classes), 3))

def draw_bounding_box(img, class_id, confidence, x, y, x_plus_w, y_plus_h):
    """
    Draws bounding boxes on the input image based on the provided arguments.

    Args:
        img (numpy.ndarray): The input image to draw the bounding box on.
        class_id (int): Class ID of the detected object.
        confidence (float): Confidence score of the detected object.
        x (int): X-coordinate of the top-left corner of the bounding box.
        y (int): Y-coordinate of the top-left corner of the bounding box.
        x_plus_w (int): X-coordinate of the bottom-right corner of the bounding box.
        y_plus_h (int): Y-coordinate of the bottom-right corner of the bounding box.
    """
    label = f"{classes[class_id]} ({confidence:.2f})"
    color = colors[class_id]
    cv2.rectangle(img, (x, y), (x_plus_w, y_plus_h), color, 2)
    cv2.putText(img, label, (x - 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)


def get_onnx_results(onnx_model, input_image):
    """
    Main function to load ONNX model, perform inference, draw bounding boxes, and display the output image.

    Args:
        onnx_model (str): Path to the ONNX model.
        input_image (str): Path to the input image.

    Returns:
        list: List of dictionaries containing detection information such as class_id, class_name, confidence, etc.
    """
    # Load the ONNX model
    model: cv2.dnn.Net = cv2.dnn.readNetFromONNX(onnx_model)

    # Read the input image
    original_image: np.ndarray = input_image
    # original_image: np.ndarray = cv2.imread(input_image)
    [height, width, _] = original_image.shape

    # Prepare a square image for inference
    length = max((height, width))
    image = np.zeros((length, length, 3), np.uint8)
    image[0:height, 0:width] = original_image

    # Calculate scale factor
    scale = length / 640

    # Preprocess the image and prepare blob for model
    blob = cv2.dnn.blobFromImage(image, scalefactor=1 / 255, size=(640, 640), swapRB=True)
    model.setInput(blob)

    # Perform inference
    outputs = model.forward()

    # Prepare output array
    outputs = np.array([cv2.transpose(outputs[0])])
    rows = outputs.shape[1]

    boxes = []
    scores = []
    class_ids = []

    # Iterate through output to collect bounding boxes, confidence scores, and class IDs
    for i in range(rows):
        classes_scores = outputs[0][i][4:]
        (minScore, maxScore, minClassLoc, (x, maxClassIndex)) = cv2.minMaxLoc(classes_scores)
        if maxScore >= params['conf_thres']:
            box = [
                outputs[0][i][0] - (0.5 * outputs[0][i][2]),
                outputs[0][i][1] - (0.5 * outputs[0][i][3]),
                outputs[0][i][2],
                outputs[0][i][3],
            ]
            boxes.append(box)
            scores.append(maxScore)
            class_ids.append(maxClassIndex)

    # Apply NMS (Non-maximum suppression)
    result_boxes = cv2.dnn.NMSBoxes(boxes, scores,  params['conf_thres'], params['iou_thres'])

    detections = []

    # Iterate through NMS results to draw bounding boxes and labels
    for i in range(len(result_boxes)):
        index = result_boxes[i]
        box = boxes[index]
        detection = OrderInfo(
            classes[class_ids[index]],
            round(box[0] * scale),
            round(box[1] * scale),
            round(box[2] * scale),
            round(box[3] * scale),
            round(box[0] * scale + (box[2] * 0.5) * scale),
            round(box[1] * scale + (box[3] * 0.5) * scale),
            scores[index]
        )
        detections.append(detection)
        # draw_bounding_box(
        #     original_image,
        #     class_ids[index],
        #     scores[index],
        #     round(box[0] * scale),
        #     round(box[1] * scale),
        #     round((box[0] + box[2]) * scale),
        #     round((box[1] + box[3]) * scale),
        # )

    # Display the image with bounding boxes

    return detections