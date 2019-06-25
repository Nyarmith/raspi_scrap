#!/usr/bin/env python

# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2

imHeight = 480
imWidth  = 640
# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (imWidth, imHeight)
camera.framerate = 60
rawCapture = PiRGBArray(camera)

# allow the camera to warmup
time.sleep(0.1)

# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    # grab the raw NumPy array representing the image, then initialize the timestamp
    # and occupied/unoccupied text
    image = frame.array
    print image.shape
    

    # show the frame
    cv2.imshow("Frame", image)
    key = cv2.waitKey(1) & 0xFF

    # clear the stream in preparation for the next frame
    rawCapture.truncate(0)

    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
        break
