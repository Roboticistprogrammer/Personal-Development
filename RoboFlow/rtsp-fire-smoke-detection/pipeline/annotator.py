import supervision as sv
import numpy as np


class Annotator:
    def __init__(self):
        self.box_annotator = sv.BoxAnnotator(thickness=1)
        self.label_annotator = sv.LabelAnnotator(
            text_position=sv.Position.BOTTOM_LEFT
        )

    def annotate(self, frame: np.ndarray, predictions: dict) -> np.ndarray:
        detections, valid_preds = self._parse_predictions(predictions, frame.shape)
        if len(detections) == 0:
            return frame

        labels = [f"{p['class']} {p['confidence']:.0%}" for p in valid_preds]
        annotated = self.box_annotator.annotate(scene=frame.copy(), detections=detections)
        return self.label_annotator.annotate(
            scene=annotated,
            detections=detections,
            labels=labels,
        )

    def _parse_predictions(self, predictions: dict, frame_shape: tuple):
        frame_height, frame_width = frame_shape[:2]
        valid_preds = []
        boxes = []
        confidences = []
        class_ids = []

        for class_id, prediction in enumerate(predictions.get("predictions", [])):
            try:
                x = float(prediction["x"])
                y = float(prediction["y"])
                width = float(prediction["width"])
                height = float(prediction["height"])
                confidence = float(prediction["confidence"])
            except (KeyError, TypeError, ValueError):
                continue

            x1 = max(0, x - width / 2)
            y1 = max(0, y - height / 2)
            x2 = min(frame_width, x + width / 2)
            y2 = min(frame_height, y + height / 2)

            if x2 <= x1 or y2 <= y1:
                continue

            valid_preds.append(prediction)
            boxes.append([x1, y1, x2, y2])
            confidences.append(confidence)
            class_ids.append(class_id)

        xyxy = np.array(boxes, dtype=np.float32).reshape(-1, 4)
        return (
            sv.Detections(
                xyxy=xyxy,
                confidence=np.array(confidences, dtype=np.float32),
                class_id=np.array(class_ids, dtype=int),
            ),
            valid_preds,
        )
