import cv2
import logging
import os
import time
from pathlib import Path

import config

from pipeline.stream_reader import StreamReader
from pipeline.inference_client import FireSmokeDetector
from pipeline.annotator import Annotator

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

TARGET_FPS = 10
FRAME_INTERVAL = 1.0 / TARGET_FPS


def load_env_file(path: str = ".env"):
    env_path = Path(path)
    if not env_path.exists():
        return

    for line in env_path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue

        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip("\"'"))


def get_setting(name: str, default=None):
    return getattr(config, name, os.getenv(name, default))


def main():
    load_env_file()

    rtsp_url = get_setting("RTSP_URL", "fire.mp4")
    api_url = get_setting("API_URL", "https://detect.roboflow.com")
    api_key = get_setting("API_KEY") or get_setting("ROBOFLOW_API_KEY")
    model_id = get_setting("MODEL_ID")
    confidence = float(get_setting("CONFIDENCE", 0.4))

    if not api_key:
        raise ValueError("Missing API_KEY or ROBOFLOW_API_KEY in config.py or environment")
    if not model_id:
        raise ValueError("Missing MODEL_ID in config.py or environment")

    reader = StreamReader(rtsp_url).start()
    detector = FireSmokeDetector(api_url, api_key, model_id, confidence)
    annotator = Annotator()
    last_inference_time = 0
    last_annotated_frame = None

    try:
        while True:
            if not reader.is_alive():
                time.sleep(1)
                continue

            frame = reader.get_frame()
            if frame is None:
                time.sleep(0.01)
                continue

            now = time.time()
            if now - last_inference_time >= FRAME_INTERVAL:
                last_inference_time = now
                predictions = detector.predict(frame)

                detected = predictions.get("predictions", [])
                if detected:
                    for d in detected:
                        logger.info(
                            f"Detected: {d['class']} | Confidence: {d['confidence']:.0%} | "
                            f"Box: ({d['x']:.0f}, {d['y']:.0f})"
                        )

                last_annotated_frame = annotator.annotate(frame, predictions)

            display_frame = last_annotated_frame if last_annotated_frame is not None else frame
            cv2.imshow("Wildfire Smoke Detection", display_frame)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    except KeyboardInterrupt:
        logger.info("Interrupted by user")
    finally:
        reader.stop()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
