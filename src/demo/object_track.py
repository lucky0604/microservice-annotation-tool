# -*- coding: utf-8 -*-
"""
@Time    : 10/21/20 6:25 PM
@Author  : Lucky
@Email   : lucky_soft@163.com
@File    : object_track.py
@Desc    : Test opencv object track demo
"""
import zipfile
import requests
from io import BytesIO
import glob
import numpy as np
import cv2
import sys
import datetime
# TODO: 1, download zip from alioss
starttime = datetime.datetime.now()
request = requests.get('http://test-images-oss.awkvector.com/3066/2020/11/13/7ad1215abcab93099d79e9bd0294dae5.zip')
file = zipfile.ZipFile(BytesIO(request.content))

# TODO: 2, extract images
file.extractall('./images')
# print(file, ' ------ zip file --------')
# TODO: 3, convert to video
img_arr = []
for filename in glob.glob('./images/*.jpg'):
    img = cv2.imread(filename)
    height, width, layers = img.shape
    size = (width, height)
    img_arr.append(img)

out = cv2.VideoWriter('./video/demo01.mp4', cv2.VideoWriter_fourcc(*'avc1'), 10, size)

for i in range(len(img_arr)):
    out.write(img_arr[i])
out.release()
# TODO: 4, return track data
(major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')
if __name__ == '__main__':
    tracker_types = ['BOOSTING', 'MIL', 'KCF', 'TLD', 'MEDIANFLOW', 'GOTURN', 'MOSSE', 'CSRT']
    tracker_type = tracker_types[2]

    if int(minor_ver) < 3:
        tracker = cv2.Tracker_create(tracker_type)
    else:
        if tracker_type == 'BOOSTING':
            tracker = cv2.TrackerBoosting_create()
        if tracker_type == 'MIL':
            tracker = cv2.TrackerMIL_create()
        if tracker_type == 'KCF':
            tracker = cv2.TrackerKCF_create()
        if tracker_type == 'TLD':
            tracker = cv2.TrackerTLD_create()
        if tracker_type == 'MEDIANFLOW':
            tracker = cv2.TrackerMedianFlow_create()
        if tracker_type == 'GOTURN':
            tracker = cv2.TrackerGOTURN_create()
        if tracker_type == 'MOSSE':
            tracker = cv2.TrackerMOSSE_create()
        if tracker_type == 'CSRT':
            tracker = cv2.TrackerCSRT_create()

    bbox = [
        {"x":190.46987951807228,"y":158.93975903614458},
        {"x":309.9759036144578,"y":158.93975903614458},
        {"x":309.9759036144578,"y":227.1807228915663},
        {"x":195.46987951807228,"y":227.1807228915663}
    ]
    video_cap = cv2.VideoCapture('./video/demo01.mp4')
    ok, frame = video_cap.read()
    if not ok:
        sys.exit()

    bbox_init = (bbox[0]['x'], bbox[0]['y'], bbox[2]['x'] - bbox[0]['x'], bbox[3]['y'] - bbox[0]['y'])
    ok = tracker.init(frame, bbox_init)
    track_result = []
    # track_index = int(payload.frame_index)
    track_index = 1
    while True:
        track_index += 1
        ok, frame = video_cap.read()
        if not ok:
            break
        ok, bbox_result = tracker.update(frame)
        p1 = {'x': bbox_result[0], 'y': bbox_result[1]}
        p2 = {'x': bbox_result[0], 'y': bbox_result[1] + bbox_result[3]}
        p3 = {'x': bbox_result[0] + bbox_result[2], 'y': bbox_result[1] + bbox_result[3]}
        p4 = {'x': bbox_result[0] + bbox_result[2], 'y': bbox_result[1]}
        rec = [p1, p2, p3, p4]
        obj = {str(track_index): rec}
        track_result.append(obj)
    endtime = datetime.datetime.now()
    costs = (endtime - starttime).seconds
    print(track_result, ' ------- track result -------')
    print(costs, ' ------------ costs -------------')