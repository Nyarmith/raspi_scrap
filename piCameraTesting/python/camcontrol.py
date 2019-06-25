

#import cv2
#from picamera.array import PiRGBArray

from picamera import PiCamera
import time


def setFixedParams(camera, iso):
    # turn on auto params
    camera.awb_mode = 'auto'
    camera.exposure_mode = 'auto'
    camera.iso = iso 
    
    # allow auto params to settle
    time.sleep(3)
    
    # fix shutter speed
    camera.shutter_speed = camera.exposure_speed
    
    # fix digital and analog gains
    camera.exposure_mode = 'off'
    
    # turn off awb, leaves awb at current val
    g = camera.awb_gains
    camera.awb_mode = 'off'
    camera.awb_gains = g


    
    print 'set camera params'
    print 'exposure {}, awbGains {}, analogGain {}, digitalGain {}'.format(
            camera.shutter_speed, 
            g, 
            camera.analog_gain, 
            camera.digital_gain)

def setAutoParams(camera, iso):
    # turn on auto params
    camera.awb_mode = 'auto'
    camera.exposure_mode = 'auto'
    camera.iso = iso 

    time.sleep(3)
    
