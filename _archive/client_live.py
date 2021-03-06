# Surveillance Project
# File: client_live.py
# Author: Ryan Anstotz
# Description:
#  Records video to send to a server
#  *** Please note to run server code prior to this script ***
#
# =================================================================================

# import necessary packages
import os
import sys
import numpy as np
import socket
import pickle
import struct
from picamera.array import PiRGBArray
from picamera import PiCamera
import time 
import cv2
import json

# import functions/classes
from config import *

# main function
def main(argv):

    # set camera specs
    height = 640
    width = 480
    framerate = 20
    
    # initialize and set camera
    print "Initializing camera..."
    camera = PiCamera()
    camera.resolution = (height, width)
    camera.framerate = framerate
    rawCapture = PiRGBArray(camera, size=(height, width))
    print "Camera initialized."
    
    # allow time for camera to warm-up
    time.sleep(0.2)

    # socket parameters
    script_type = "server"
    #data_file = argv[1]
    #HOST, PORT = parse_config(data_file, script_type)
    host = '18.214.123.134'
    port = 5050

    print "Host IP: ", host
    print "at Port: ", port

   
    # initialize socket connections
    print "Initializing socket..."
    clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientsocket.connect((host, port))
    print "Socket initialized."

    test_flag = False
    
    # capture frames from camera
    for frame in camera.capture_continuous(rawCapture, format="bgr",
                                           use_video_port=True):

        if test_flag == False:
            print "capturing images..."
            test_flag = True
            
        # grab raw Numpy array representing the image, then
        # initialize timestamp and text
        image = frame.array

        # serialize data
        data = pickle.dumps(image)

        # send data over socket in binary form
        clientsocket.sendall(struct.pack("=L", len(data))+data)
                
        # clear the stream in preparation for the next frame
        rawCapture.truncate(0)

    # return from main
    return



# execute 
if __name__ == "__main__":
    main(sys.argv[:])

# end of file
