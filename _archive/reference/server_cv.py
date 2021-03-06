# Surveillance Project
# File: server_cv.py
# Author: Ryan Anstotz
# Description:
#  Receives stream over socket, stores stream
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
 
# main function
def main(argv):

    # set host and port for socket
    HOST = ''
    PORT = 8089
    
    # initialize socket connections
    print "Creating socket..."
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print "Socket created."

    # bind socket
    s.bind((HOST, PORT))
    print "Socket bind complete."
    s.listen(10)
    print "Socket now listening."

    # accept connection
    conn, addr = s.accept()
    print "Socket connected to IP:", addr[0]
    
    # data prep. 'L' stands for unsigned long
    data = ""
    payload_size = struct.calcsize("=L")
    print "payload_size is: ", sys.getsizeof(payload_size)
    
    one_time = False
    
    # accept data continuously
    while (1):
        
        # get and process the payload
        while len(data) < payload_size:
            data += conn.recv(4096)
        print "len of data is: ", len(data)
        
        if one_time == False:
            print "len of data is: ", len(data)
            
        packed_msg_size = data[:payload_size]
        data = data[payload_size:]
        msg_size = struct.unpack("=L", packed_msg_size)[0]
        print "len of message size is: ", msg_size
        
        if one_time == False:
            print "len of msg_size is: ", msg_size
            one_time = True
            
        while len(data) < msg_size:
            data += conn.recv(4096)
        frame_data = data[:msg_size]
        data = data[msg_size:]
        print "about to pickle!"
        
        # load image
        image = pickle.loads(frame_data)

        # display the stream
        cv2.imshow("Frame", image)
        key = cv2.waitKey(1) & 0xFF

        # if 'q' key pressed, break from loop
        if key == ord("q"):
            break
    
    # return from main
    return

# execute 
if __name__ == "__main__":
    main(sys.argv[:])

# end of file
