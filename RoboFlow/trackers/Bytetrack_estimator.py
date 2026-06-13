import cv2

import supervision as sv
from inference import get_model
from trackers import ByteTrackTracker
from trackers.utils.state_representations import (
    XCYCSRStateEstimator,
    XYXYStateEstimator,
)

model = get_model("rfdetr-nano")

tracker_xyxy = ByteTrackTracker(
    state_estimator_class=XYXYStateEstimator,
)
tracker_xcycsr = ByteTrackTracker(
    state_estimator_class=XCYCSRStateEstimator,
)

cap = cv2.VideoCapture("soccer.mp4")
while True:
    ret, frame = cap.read()
    if not ret:
        break

    result = model.infer(frame)[0]
    detections = sv.Detections.from_inference(result)

    tracked_xyxy = tracker_xyxy.update(detections)
    tracked_xcycsr = tracker_xcycsr.update(detections)

    # Compare tracker_id assignments, box smoothness, etc.
    print(f"XYXY IDs:   {tracked_xyxy.tracker_id}")
    print(f"XCYCSR IDs: {tracked_xcycsr.tracker_id}")