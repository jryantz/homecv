import cv2
from ultralytics import YOLO
from homecv.config import Config


def analyze_snapshot(snapshot, zone, desired_class):
    model = YOLO(Config.MODEL_PATH)
    results = model(snapshot)[0]

    detected = False
    for box, cls in zip(results.boxes.xyxy, results.boxes.cls):
        if int(cls) != desired_class:
            continue

        x1, y1, x2, y2 = map(int, box)

        # Draw the 'detected' area
        cv2.rectangle(snapshot, (x1, y1), (x2, y2), (0, 255, 0), 2)

        # Check intersection with zone
        dx1, dy1, dx2, dy2 = zone
        if x1 >= dx2 or x2 <= dx1 or y1 >= dy2 or y2 <= dy1:
            # No overlap
            continue

        detected = True

    return detected, snapshot
