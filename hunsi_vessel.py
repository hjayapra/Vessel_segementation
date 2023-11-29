# -*- coding: utf-8 -*-
"""Hunsi_Vessel.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1c7BWOEdh-6ZN8z4U4rOZJ4xvlQl4QOcQ
"""

from google.colab import drive
drive.mount("/content/drive")

import glob, gzip, os
import nibabel as nib, numpy as np

STORAGE_PATH = os.path.join("drive", "MyDrive", "BrainVeins-20230201T142415Z-002" , "BrainVeins", "datafolder")
DATA_PATH = os.path.join(STORAGE_PATH, "data")
SHAPE=(50, 150, 11)
MAX_VEINS=100
SKIP=10

STORAGE_PATH

def item(l):
  if len(l) == 1:
    return l[0]
  else:
    return None

for scandir in scandirs:
    for box in ["left", "right"]:
      image_file = item(glob.glob(os.path.join(scandir, "*_SWI_TE1_" + box + "box.nii.gz")))
      path_txt_file = item(glob.glob(os.path.join(scandir, "*_TE1_" + box + "box_path.txt.gz")))

      if not (image_file and path_txt_file):
        continue

      image_npy_file = image_file[: -len(".nii.gz")] + ".npy"
      path_npy_file = path_txt_file[: -len(".txt.gz")] + ".npy"

      image = np.array(nib.load(image_file).dataobj)
      image.resize(SHAPE)
      path_image = np.zeros((MAX_VEINS,) + SHAPE)

      truncated_paths = set()
      with gzip.open(path_txt_file) as lines:
        for line in lines:
          line = [int(n) for n in line.split()]
          line = np.split(np.array(line), len(line) // 3)
          line = line[SKIP:]
          line = { tuple(point) for point in line }
          truncated_paths.add(tuple(line))

      for i, path in enumerate(truncated_paths):
        for x, y, z in path:
          path_image[i, x, y, z] = 1

      np.save(image_npy_file, image)
      np.save(path_npy_file, path_image)
      print(image_npy_file)
      print(path_npy_file)

scandirs = sorted(glob.glob(os.path.join(DATA_PATH, "*/*/step03_SWI/TE1/")))
for dir in scandirs:
  print(dir)

"""VESSEL MASK SEGMENTATION"""

!pip install -qU "monai[ignite, nibabel, torchvision, tqdm]==0.6.0"

import copy, glob, gzip, os, random

import nibabel as nib, numpy as np, torch

import monai
from monai.config import print_config

print_config()

!nvidia-smi

device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using {device} device")

#Steps
STORAGE_PATH = os.path.join("drive", "MyDrive", "BrainVeins-20230201T142415Z-002", "BrainVeins")
DATA_PATH = os.path.join(STORAGE_PATH, "data")
SHAPE=(50, 150, 11)
MAX_VEINS=100
SKIP=10
MODEL_PATH = os.path.join(STORAGE_PATH, "BrainVeinsModel.pth")

MODEL_PATH

train_images = sorted(
  glob.glob(os.path.join(MODEL_PATH, "*/*/step03_SWI/TE1/*box.npy.gz.npy"))
)
train_labels = sorted(
  glob.glob(os.path.join(MODEL_PATH, "*/*/step03_SWI/TE1/*box_path.npy.gz.npy"))
)
data_dicts = [
  {"image": image_file, "label": label_file}
  for image_file, label_file in zip(train_images, train_labels)
]

val_count = len(data_dicts) // 3
train_files, val_files = data_dicts[:-val_count], data_dicts[-val_count:]


#Check to see values
print(val_count)
print(f"{len(train_files)} training files")
print(f"{len(val_files)} validation files")

#drive.flush_and_unmount()