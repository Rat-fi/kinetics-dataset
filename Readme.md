# Kinetics 400 Validation-Set Downloader

Kinetics is a collection of large-scale, high-quality datasets of URL links of up to 650,000 video clips that cover 400/600/700 human action classes, depending on the dataset version. The videos include human-object interactions such as playing instruments, as well as human-human interactions such as shaking hands and hugging. Each action class has at least 400/600/700 video clips. Each clip is human annotated with a single action class and lasts around 10 seconds.

The bash script is derived from the official Common Visual Data Foundation downloader, that can be found here: https://github.com/cvdfoundation/kinetics-dataset

This downloader retrieves the official kinetics-400 **validation set**, made of 19881 videos, and optionally cleans the dataset from the officialy listed corrupted videos, aswell as the ones detected by OpenCV.

## Validation-Set Information

Nb of videos: 19881

Nb of corrupted videos from annotations "is_cc": 519

Nb of corrupted videos from OpenCV: 4

## How To Use: 

### Clone repo and enter directory
```
git clone https://github.com/rat-fi/kinetics-dataset.git
cd kinetics-dataset
```


### Download and extract the videos + annotations
This will create three directories:
- `k400/targz`: Tar gzips of the videos, you can delete this after the execution is done.
- `k400/val`: extracted videos will be here.
- `k400/annotations`: includes a csv file with the annotations for each video in the /val folder.
```
bash ./download_k400_val.sh
```


## Optional: Clean Dataset:

This will remove the 514 videos flagged as corrupt by the official kinetics dataset, aswell as the 4 videos that are detected corrupt by OpenCV. 

**They will not be deleted, they will be moved out of the `k400/val` folder to `k400/corrupted`**

### Create virtual environment
Windows: 
```
python -m venv venv
venv\Scripts\activate.bat
```
Linux:
```
python3 -m venv venv
source venv/bin/activate
```

### Install python dependencies
```
pip install opencv-python pandas tqdm
```

### Run the python file
```
python remove_corrupted_videos.py
```
