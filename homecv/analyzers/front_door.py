import cv2
import numpy as np
from homecv.analyzers.base import analyze_snapshot
from homecv.integrations.hass.client import HomeAssistantClient
from homecv.snapshots.storage import store_snapshot


def analyze_snapshot_for_person_at_front_door(snapshot):
    zone = (80, 250, 400, 500)
    # Class 0 is 'person' in the YOLO model
    desired_class = 0
    detected, snapshot = analyze_snapshot(snapshot, zone, desired_class)

    # Draw the 'zone' area
    cv2.rectangle(snapshot, (zone[0], zone[1]), (zone[2], zone[3]), (255, 0, 0), 2)

    return detected


def check(client: HomeAssistantClient, debug: bool = False):
    snapshot = client.get_snapshot("camera.front_yard_snapshots_fluent")

    img = cv2.imdecode(np.frombuffer(snapshot, np.uint8), cv2.IMREAD_COLOR)
    detected = analyze_snapshot_for_person_at_front_door(img)

    if debug:
        store_snapshot(snapshot, "originals")
        store_snapshot(img, "snapshots")

    return detected
