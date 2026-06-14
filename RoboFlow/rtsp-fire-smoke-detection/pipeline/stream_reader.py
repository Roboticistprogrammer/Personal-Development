import logging
import threading
import time

import cv2

logger = logging.getLogger(__name__)


class StreamReader:
    def __init__(self, rtsp_url: str, reconnect_delay: int = 5, watchdog_timeout: int = 10):
        self.rtsp_url = rtsp_url
        self.reconnect_delay = reconnect_delay
        self.watchdog_timeout = watchdog_timeout
        self.frame = None
        self.last_frame_time = None
        self.running = False
        self.cap = None
        self.fps = 30.0
        self._lock = threading.Lock()
        self._thread = None

    def start(self):
        self.running = True
        self._thread = threading.Thread(target=self._read_loop, daemon=True)
        self._thread.start()
        return self

    def get_frame(self):
        with self._lock:
            return self.frame

    def is_alive(self):
        if self.last_frame_time is None:
            return False

        return (time.time() - self.last_frame_time) < self.watchdog_timeout

    def stop(self):
        self.running = False
        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=2)
        if self.cap:
            self.cap.release()
            self.cap = None

    def _connect(self):
        if self.cap:
            self.cap.release()

        self.cap = cv2.VideoCapture(self.rtsp_url, cv2.CAP_FFMPEG)
        if not self.cap.isOpened():
            return False

        self.fps = self.cap.get(cv2.CAP_PROP_FPS) or 30.0
        return True

    def _read_loop(self):
        while self.running:
            if not self._connect():
                time.sleep(self.reconnect_delay)
                continue
            frame_interval = 1.0 / self.fps
            while self.running:
                start = time.time()
                ret, frame = self.cap.read()

                if not ret:
                    self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                    ret, frame = self.cap.read()
                    if not ret:
                        break

                with self._lock:
                    self.frame = frame
                    self.last_frame_time = time.time()

                elapsed = time.time() - start
                sleep_time = frame_interval - elapsed
                if sleep_time > 0:
                    time.sleep(sleep_time)

            time.sleep(self.reconnect_delay)
