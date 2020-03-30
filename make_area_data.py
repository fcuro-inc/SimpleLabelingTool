#! /usr/bin/env python
# -*- coding:utf-8 -*-

import numpy as np
import cv2
import os
import glob
import readchar
import argparse
import json

parser = argparse.ArgumentParser()
parser.add_argument(
    "image_dir",
    help = "Image Directory Path(jpg)."
)
args = parser.parse_args()
im_dir = args.image_dir

images = glob.glob("%s/*.jpg"%im_dir)

drawing = False # true if mouse is pressed
SAVE = 1 # true if annotaion is saved
ix,iy = -1,-1
ox,oy = -1,-1

# mouse callback function
def draw_area(event,x,y,flags,param):
    global ix,iy,ox,oy,drawing,mode
    img = param
    img2 = np.copy(img)
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix,iy = x,y
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        ox,oy = x,y
        cv2.rectangle(img2,(ix,iy),(ox,oy),(0,0,255),1)
        print "rect maked!"
        cv2.imshow("img", img2)


# "q" key => exit
# "b" key => save and go next image
# "n" key => not save and go next image
# "o" key => record area annotation
# else => cancel area annotation and make again
def make_annotation(img):
    global SAVE
    areas_list = []
    while 1:
        cv2.imshow("img", img)
        k = cv2.waitKey(0)
        if k == ord('q'):
            exit()
        elif k == ord('b'):
            break
        elif k == ord('n'):
            SAVE = 0
            break
        elif k == ord('o'):
            cv2.rectangle(img,(ix,iy),(ox,oy),(0,0,255),1)
            if ix < ox:
                area_dict = {"xmin":ix, "ymin":iy, "xmax":ox, "ymax":oy}
            else:
                area_dict = {"xmin":ox, "ymin":oy, "xmax":ix, "ymax":iy}
            areas_list.append(area_dict)
        else:
            print "area_rect canceled"
    cv2.destroyAllWindows()
    return areas_list


def save_json(image, annotation_dict):
    if (SAVE == 1):
        imagedir, imagename = os.path.split(os.path.dirname(image))
        if not os.path.isdir("./area_annotations/%s"%imagename):
            os.makedirs("./area_annotations/%s"%imagename)
        name,ext = os.path.splitext(os.path.basename(image))
        with open("./area_annotations/%s/%s.json"%(imagename,name), 'w') as f:
            json.dump(annotation_dict, f, sort_keys=True)
        print "saved %s.json"%name

def is_annotated(image):
    imagedir, imagename = os.path.split(os.path.dirname(image))
    name,ext = os.path.splitext(os.path.basename(image))
    if os.path.exists("./area_annotations/%s/%s.json"%(imagename,name)):
        return True
    else:
        return False

def get_new_size(width, height, thresh):
    if width < height:
        new_width = thresh
        new_height = new_width * height/width
    else:
        new_height = thresh
        new_width = new_height * width/height
    return new_width, new_height

if __name__ == '__main__':
    for image in images:
        if is_annotated(image):
            print "%s is already annotated!"%os.path.basename(image)
            continue
        SAVE = 1
        annotation_dict = {}
        img = cv2.imread(image, cv2.IMREAD_COLOR)


        ## write size infomation
        height, width, depth = img.shape[:3]
        size_dict = {"width": width, "height":height, "depth":depth}
        annotation_dict["size"] = size_dict

        ## GUI operation
        cv2.namedWindow("img", cv2.WINDOW_NORMAL)
        cv2.setMouseCallback('img',draw_area, img)
        areas_list = make_annotation(img)

        ## complete to make json and save
        annotation_dict["areas"] = areas_list
        print annotation_dict
        save_json(image, annotation_dict)
