#!/usr/bin/env python
import cv2
import os

count=1
vid = 'http://test-images-oss.awkvector.com/mp4/3048/2020/11/c49fc7d12de3d2b8af6b18445e8638a9.mp4'
vidcap = cv2.VideoCapture(vid)
def getFrame(sec):
    vidcap.set(cv2.CAP_PROP_POS_MSEC,sec*1000)
    hasFrames,image = vidcap.read()
    if hasFrames:
        cv2.imwrite("./images/"+str(count)+".jpg", image) # Save frame as JPG file
    return hasFrames
sec = 0
frameRate = 0.1 # Change this number to 1 for each 1 second

success = getFrame(sec)
while success:
    count = count + 1
    sec = sec + frameRate
    sec = round(sec, 2)
    success = getFrame(sec)