#! /usr/bin/env python
# -*- coding:utf-8 -*-

import glob
import shutil
import os
import argparse
import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument(
    "dataset_path",
    help = "dataset name with full path."
)
parser.add_argument(
    "image_dir",
    help = "Image source directory"
)
parser.add_argument(
    "class_num",
    help = "number of classes"
)
args = parser.parse_args()
dataset_name = args.dataset_path
image_dir = args.image_dir
cls_num = int(args.class_num)

# make structure of dataset directory
if not os.path.isdir("%s"%dataset_name):
    os.makedirs("%s"%dataset_name)
    os.makedirs("%s/datasets/Annotations"%dataset_name)
    os.makedirs("%s/datasets/ImageSets/Main"%dataset_name)
    os.makedirs("%s/datasets/JPEGImages"%dataset_name)
    os.makedirs("%s/output"%dataset_name)

with open("%s/datasets/category.txt"%dataset_name, 'w') as f:
    f.writelines("id\tname")
    for i in range(1,cls_num+1):
        f.writelines("%d\t%s"%(i,str(i).zfill(3)))

annotations = glob.glob("./annotations/*/*.xml")
for annotation in annotations:
    name, ext = os.path.splitext(os.path.basename(annotation))
    image = glob.glob("%s/*/%s.jpg"%(image_dir, name))[0]
    shutil.copy(annotation, "%s/datasets/Annotations"%dataset_name)
    shutil.copy(image, "%s/datasets/JPEGImages"%dataset_name)
    if np.random.rand() < 0.9:
        with open("%s/datasets/ImageSets/Main/trainval.txt"%dataset_name, 'a') as f:
            f.writelines("%s\n"%name)
    else:
        with open("%s/datasets/ImageSets/Main/test.txt"%dataset_name, 'a') as f:
            f.writelines("%s\n"%name)
