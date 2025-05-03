#!/usr/bin/env python3
import cv2
import os
import shutil
import pandas as pd
from glob import glob
from multiprocessing import cpu_count
from tqdm.contrib.concurrent import process_map

# === Settings ===
VIDEO_DIR     = './k400/val'
VAL_CSV_PATH  = './k400/annotations/val.csv'
CORRUPTED_DIR = './k400/corrupted'

# === Load annotations & build filename set ===
val_df = pd.read_csv(VAL_CSV_PATH)
val_df['filename'] = val_df.apply(
    lambda r: f"{r['youtube_id']}_{r['time_start']:06}_{r['time_end']:06}.mp4",
    axis=1
)

# === Gather all video paths ===
video_paths = sorted(glob(os.path.join(VIDEO_DIR, '*.mp4')))

def check_video(path):
    """
    Returns (filename, is_corrupted)
    """
    fname = os.path.basename(path)
    cap = cv2.VideoCapture(path)
    if not cap.isOpened():
        corrupted = True
    else:
        frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT) or 0
        if frame_count <= 0:
            corrupted = True
        else:
            ret, frame = cap.read()
            corrupted = not (ret and frame is not None)
    cap.release()
    return fname, corrupted

if __name__ == '__main__':
    os.makedirs(CORRUPTED_DIR, exist_ok=True)

    # 1) Move Kinetics-flagged CC videos
    cc_filenames = set(val_df[val_df['is_cc'] == 1]['filename'])
    moved_cc = 0
    for fname in cc_filenames:
        src = os.path.join(VIDEO_DIR, fname)
        if os.path.exists(src):
            try:
                shutil.move(src, os.path.join(CORRUPTED_DIR, fname))
                moved_cc += 1
            except Exception as e:
                print(f"Failed to move CC video {fname}: {e}")

    # record original total before filtering
    original_total = len(video_paths)

    # filter out CC videos for the scan
    video_paths = [
        p for p in video_paths
        if os.path.basename(p) not in cc_filenames
    ]

    # 2) Check remaining videos
    results = process_map(
        check_video,
        video_paths,
        max_workers=cpu_count(),
        chunksize=1,
        desc="Checking videos"
    )

    # collect newly detected corrupted
    corrupted = [fn for fn, corr in results if corr]

    # 3) Move newly detected corrupted into same folder
    moved_ocv = 0
    for fn in corrupted:
        src = os.path.join(VIDEO_DIR, fn)
        if os.path.exists(src):
            try:
                shutil.move(src, os.path.join(CORRUPTED_DIR, fn))
                moved_ocv += 1
            except Exception as e:
                print(f"Failed to move corrupted video {fn}: {e}")

    # compute how many remain
    videos_left = original_total - moved_cc - moved_ocv

    # Summary
    print(f"\nTotal videos detected:       {original_total}")
    print(f"Kinetics-flagged CC moved:   {moved_cc}  → {CORRUPTED_DIR}")
    print(f"OpenCV-detected corrupt:     {moved_ocv}  → {CORRUPTED_DIR}")
    print(f"Videos remaining:             {videos_left}")
