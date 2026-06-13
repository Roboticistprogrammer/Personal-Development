# Roboflow trackers Library Demos

Please check [here](https://trackers.roboflow.com/latest/learn/install/) for details.


i have used: 

for seq_dir in ./mot17/val/MOT17-*-FRCNN; do
    seq_name=$(basename "$seq_dir")

    trackers track \
        --detections "$seq_dir/det/det.txt" \
        --tracker bytetrack \
        --mot-output "results/${seq_name}.txt"
done

in "bash", to create .txt files in results folder.

## Demo Video

<video controls width="640" src="soccer.mp4"></video>

Example tracking output on soccer video using ByteTrack.

