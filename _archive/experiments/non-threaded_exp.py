# Surveillance Project
# File: video_capture_exp.py
# Author: Ryan Anstotz
# Description:
#  Benchmark speed of video capture framerate
# =================================================================================

# import necessary packages
import os
import sys
from picamera.array import PiRGBArray
from picamera import PiCamera
import time 
import cv2
import argparse

# main function
def main(argv):

    # get args
    ap = argparse.ArgumentParser()
    ap.add_argument("-f", "--frames", type=int, default=100)
    args = vars(ap.parse_args())
    
    # initialize camera
    camera = PiCamera()
    print "Initialized camera..."
    
    # set params
    height = 640
    width = 480
    camera.resolution = (640, 480)
    camera.framerate = 30
    rawCapture = PiRGBArray(camera, size=(640, 480))
    
    # warm up camera
    time.sleep(0.8)
    print "Starting video capture... "
    
    start = time.time()
    frameCounter = 0
    
    # capture frames from camera
    for frame in camera.capture_continuous(rawCapture, format="bgr",
                                           use_video_port=True):
        # grab raw Numpy array representing the image, then
        # initialize timestamp and text
        image = frame.array

        # show the frame
        #cv2.imshow("Frame", image)
        #key = cv2.waitKey(1) & 0xFF

        # clear the stream in preparation for the next frame
        rawCapture.truncate(0)

        frameCounter += 1
        if frameCounter == args["frames"]:
            break

    end = time.time()
    elapsed_time = end - start

    print "frames: ", frameCounter
    print "time:   ", elapsed_time
    print "FPS:    ", float(frameCounter) / elapsed_time
        
    return


if __name__ == "__main__":
    main(sys.argv[:])


