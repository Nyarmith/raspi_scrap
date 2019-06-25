#!/usr/bin/env python

# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2

def nothing(x):
    pass

class ParamSlider():
    def __init__(self):
        self.name = 'iso'
        cv2.namedWindow(self.name)
        cv2.createTrackbar(self.name, self.name, 0, 800, nothing)

    def getIso(self):
        return cv2.getTrackbarPos(self.name, self.name)

imHeight = 480
imWidth  = 640

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
rawCapture = PiRGBArray(camera)

camera.resolution = (imWidth, imHeight)

# set camera parameters
# max exposure capped by fps
camera.framerate = 10
# start w/ iso, basically gain

isoSlider = ParamSlider()

# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    # grab the raw NumPy array representing the image, then initialize the timestamp
    # and occupied/unoccupied text
    
    camera.iso = isoSlider.getIso()
    
    exposureSpeed = camera.exposure_speed
    awbGains = camera.awb_gains
    analogGain = camera.analog_gain
    digitalGain = camera.digital_gain

    print 'exposure {}, awbGains {}, analogGain {}, digitalGain {}'.format(exposureSpeed, awbGains, analogGain, digitalGain)

    # show the frame
    cv2.imshow("Frame", frame.array)
    key = cv2.waitKey(1) & 0xFF

    # clear the stream in preparation for the next frame
    rawCapture.truncate(0)

    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
        break
