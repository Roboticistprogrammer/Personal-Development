# Modified (RTPS)[Process RTSP Streams for Real-Time Video Analytics] Video Analytics on Jetson

I have hetpack 6.1 on my jetson so:
docker run -d \
  --name inference-server \
  --runtime nvidia \
  -p 9001:9001 \
  -v ${HOME}/.inference/cache:/tmp:rw \
  roboflow/roboflow-inference-server-jetson-6.2.0:latest
This container is used.

The approach here uses two tools: MediaMTX as a lightweight RTSP server and FFmpeg to push a video file into it as a looping stream.

ffmpeg -re -stream_loop -1 -i fire.mp4 \
  -c:v libx264 -preset ultrafast -tune zerolatency \
  -c:a aac -f rtsp rtsp://localhost:8554/stream