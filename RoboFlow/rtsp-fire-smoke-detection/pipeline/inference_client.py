import logging

import numpy as np
from inference_sdk import InferenceHTTPClient

logger = logging.getLogger(__name__)


class FireSmokeDetector:
    def __init__(self, api_url: str, api_key: str, model_id: str, confidence: float = 0.4):
        self.model_id = model_id
        self.confidence = confidence
        self.client = InferenceHTTPClient(
            api_url=api_url,
            api_key=api_key,
        )

    def predict(self, frame: np.ndarray) -> dict:
        try:
            result = self.client.infer(frame, model_id=self.model_id)
            result["predictions"] = [
                p
                for p in result.get("predictions", [])
                if p["confidence"] >= self.confidence
            ]
            return result
        except Exception as exc:
            logger.error("Inference error: %s", exc)
            return {"predictions": []}
