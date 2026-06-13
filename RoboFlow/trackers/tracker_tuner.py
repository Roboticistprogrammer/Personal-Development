from pathlib import Path
from tempfile import TemporaryDirectory

from trackers.tune import Tuner

sequence = "MOT17-02-FRCNN"
sequence_dir = Path("data/mot17/val") / sequence


def main() -> None:
    with TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        gt_dir = tmp_path / "gt"
        detections_dir = tmp_path / "detections"
        gt_dir.mkdir()
        detections_dir.mkdir()

        (gt_dir / f"{sequence}.txt").symlink_to(
            (sequence_dir / "gt" / "gt.txt").resolve()
        )
        (detections_dir / f"{sequence}.txt").symlink_to(
            (sequence_dir / "det" / "det.txt").resolve()
        )

        tuner = Tuner(
            tracker_id="bytetrack",
            gt_dir=gt_dir,
            detections_dir=detections_dir,
            objective="HOTA",
            metrics=["CLEAR", "HOTA", "Identity"],
            n_trials=50,
        )

        best_params = tuner.run()
        print(best_params)


if __name__ == "__main__":
    main()
