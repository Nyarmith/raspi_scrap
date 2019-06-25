#!/usr/bin/env python

# import the necessary packages
from picamera.array import PiYUVArray
from picamera import PiCamera
import time
import cv2

import camcontrol

###############################################
################### CONFIG ####################
outputDir = '/home/pi/Desktop/c0/'

imHeight = 480*4
imWidth  = 640*4

fps = 5
iso = 800 # options are 100, 200, 320, 400, 500, 640, 800
# higher iso = more noise, but shorter exposures

###############################################


# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
rawCapture = PiYUVArray(camera)

camera.resolution = (imWidth, imHeight)
camera.framerate = fps

# set fixed image capture settings
camcontrol.setAutoParams(camera, iso)

# capture frames from the camera
for i, frame in enumerate(camera.capture_continuous(rawCapture, format="yuv")):
    # grab the raw NumPy array representing the image, then initialize the timestamp
    # and occupied/unoccupied text
    yuvImage = frame.array
    yImage, u, v = cv2.split(yuvImage)
    
    resizedY = cv2.resize(yImage, (imWidth/2, imHeight/2))
    cv2.imshow('greyscale', resizedY)
    # show the frame
    key = cv2.waitKey(3) & 0xFF

    # clear the stream in preparation for the next frame
    rawCapture.truncate(0)

    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
        break
    
    fileName = outputDir + str(i) + '.png'
    cv2.imwrite(fileName, yImage)

    if i%5 == 0:
        print i

