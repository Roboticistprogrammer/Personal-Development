import trackers 

from trackers import Dataset, DatasetAsset, DatasetSplit, download_dataset

download_dataset(
    dataset=Dataset.MOT17,
    split=DatasetSplit.VAL,
    asset=[DatasetAsset.ANNOTATIONS, DatasetAsset.DETECTIONS],
    output="./data",
)