#! /usr/bin/env python
# -*- coding:utf-8 -*-

import numpy as np
import cv2
import os
import glob
import readchar
import argparse
import json
import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom

parser = argparse.ArgumentParser()
parser.add_argument(
    "image_dir",
    help = "Image Directory Path(jpg)."
)
args = parser.parse_args()
im_dir = args.image_dir
## ラベル付け様ID
CLASS_ID = 0

def make_xml(annotaion):
    with open(annotaion, 'r') as f:
        annotaion_json = json.load(f)
    root = ET.Element('annotation')
    folder = ET.SubElement(root, 'foler')
    folder.text = im_dir

    name,ext = os.path.splitext(os.path.basename(annotaion))
    query_path, query = os.path.split(os.path.dirname(annotaion))
    image = "../image_gathering/images/%s/%s.jpg"%(query,name)

    filename = ET.SubElement(root, 'filename')
    filename.text = os.path.basename(image)
    size = ET.SubElement(root, 'size')
    wdt = ET.SubElement(size, 'width')
    wdt.text = str(annotaion_json["size"]["width"])
    hgt = ET.SubElement(size, 'height')
    hgt.text = str(annotaion_json["size"]["height"])
    dph = ET.SubElement(size, 'depth')
    dph.text = str(annotaion_json["size"]["depth"])

    seg = ET.SubElement(root, 'segmented')
    seg.text = '0'

    img = cv2.imread(image, cv2.IMREAD_COLOR)
    for area in annotaion_json["areas"]:
        CLASS_ID = 0
        obj = ET.SubElement(root, 'object')
        img2 = np.copy(img)
        cv2.destroyAllWindows()
        cv2.rectangle(img2,(area["xmin"],area["ymin"]),(area["xmax"],area["ymax"]),(0,0,255),1)
        while 1:
            cv2.imshow("img", img2)
            k = cv2.waitKey(0)
            if k == ord('q'):
                exit()
            ## CLASS ID 1~8 (see ./class_list.txt)
            elif k >= ord('1') and k <= ord('8'):
                CLASS_ID = k - ord('0')
                print CLASS_ID
                break
            else:
                print "Please labeling again"
        nm = ET.SubElement(obj, 'name')
        nm.text =  str(CLASS_ID).zfill(3)
        ps = ET.SubElement(obj, 'pose')
        ps.text = 'Unspecified'
        tr = ET.SubElement(obj, 'truncated')
        tr.text = '0'
        di = ET.SubElement(obj, 'difficult')
        di.text = '0'
        bbox = ET.SubElement(obj, 'bndbox')
        xi = ET.SubElement(bbox, 'xmin')
        xi.text = str(area["xmin"])
        yi = ET.SubElement(bbox, 'ymin')
        yi.text = str(area["ymin"])
        xa = ET.SubElement(bbox, 'xmax')
        xa.text = str(area["xmax"])
        ya = ET.SubElement(bbox, 'ymax')
        ya.text = str(area["ymax"])
        cv2.destroyAllWindows()

    if not os.path.isdir("./annotations/%s"%query):
        os.makedirs("./annotations/%s"%query)
    xml_str = minidom.parseString(ET.tostring(root, 'utf-8')).toprettyxml(indent='    ')
    with open("./annotations/%s/%s.xml"%(query,name), 'w') as f:
        f.write(xml_str)

def get_new_size(width, height, thresh):
    if width < height:
        new_width = thresh
        new_height = new_width * height/width
    else:
        new_height = thresh
        new_width = new_height * width/height
    return new_width, new_height

def is_annotated(annotaion):
    ano_dir, ano_name = os.path.split(os.path.dirname(annotation))
    name,ext = os.path.splitext(os.path.basename(annotaion))
    if os.path.exists("./annotations/%s/%s.xml"%(ano_name,name)):
        return True
    else:
        return False


if __name__ == '__main__':
    dirpath, dirname = os.path.split(im_dir)
    annotaions = glob.glob("./area_annotations/%s/*.json"%dirname)
    for annotation in annotaions:
        if is_annotated(annotation):
            print "%s is already annotated!"%os.path.basename(annotation)
            continue
        make_xml(annotation)
