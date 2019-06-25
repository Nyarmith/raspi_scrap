#!/usr/bin/env python

# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2


###############################################
################### CONFIG ####################
imHeight = 480
imWidth  = 640

fps = 30
iso = 800
exposureTime = int(1000000.0 * 1.0 / 60.0)
autoWhiteBalance = (int(267/256), int(505/256))

###############################################


def nothing(x):
    pass

class HSVTrackbars():
    def __init__(self):
        self.name = 'HSV Threshold'
        cv2.namedWindow(self.name)
        cv2.createTrackbar('H max', self.name, 0, 255, nothing)
        cv2.createTrackbar('H min', self.name, 0, 255, nothing)
        cv2.createTrackbar('S max', self.name, 0, 255, nothing)
        cv2.createTrackbar('S min', self.name, 0, 255, nothing)
        cv2.createTrackbar('V max', self.name, 0, 255, nothing)
        cv2.createTrackbar('V min', self.name, 0, 255, nothing)
    
    def getMax(self):
        hmax = cv2.getTrackbarPos('H max', self.name) 
        smax = cv2.getTrackbarPos('S max', self.name) 
        vmax = cv2.getTrackbarPos('V max', self.name)  
        return (hmax, smax, vmax)

    def getMin(self):
        hmin = cv2.getTrackbarPos('H min', self.name) 
        smin = cv2.getTrackbarPos('S min', self.name) 
        vmin = cv2.getTrackbarPos('V min', self.name)  
        return (hmin, smin, vmin)


# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
rawCapture = PiRGBArray(camera)

camera.resolution = (imWidth, imHeight)
camera.framerate = fps

camera.awb_mode = 'off'

camera.iso = iso 
camera.shutter_speed = exposureTime
camera.awb_gains = autoWhiteBalance

# allow the camera to warmup
time.sleep(3)
# fix gains. Can't fix directly
#digital_gain and analog_gain
camera.exposure_mode = 'off'


hsvTrackbars = HSVTrackbars()

startTime = time.time()
# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    # grab the raw NumPy array representing the image, then initialize the timestamp
    # and occupied/unoccupied text

    # always blur image to start
    image = cv2.GaussianBlur(frame.array, (5, 5), 0)
    
    hsvImage = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsvImage, hsvTrackbars.getMin(), hsvTrackbars.getMax())
	
    M = cv2.moments(mask)
    if M['m00']:
        cX = int(M['m10'] / M['m00'])
        cY = int(M['m01'] / M['m00'])
    else:
        cX = 0
        cY = 0

    cv2.circle(image, (cX, cY), 5, (255,255,255), -1)
    cv2.putText(image, "centroid", (cX - 25, cY - 25),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

    
    cv2. imshow('Mask', mask)

    # show the frame
    cv2.imshow("Frame", image)
    key = cv2.waitKey(3) & 0xFF

    # clear the stream in preparation for the next frame
    rawCapture.truncate(0)

    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
        break

    endTime = time.time()
    print endTime - startTime
    startTime = endTime
