import cv2
import numpy as np
from datetime import datetime
from pathlib import Path

SNAPSHOT_DIR = Path("./images")


def create_dir(file):
    file.parent.mkdir(parents=True, exist_ok=True)
    file.touch(exist_ok=True)


def store_snapshot(data, folder):
    file = SNAPSHOT_DIR / folder / f"{datetime.now().strftime('%Y%m%d%H%M%S')}.jpg"
    create_dir(file)

    if isinstance(data, np.ndarray):
        cv2.imwrite(str(file), data)
    else:
        with open(file, "wb") as f:
            f.write(data)

    return
