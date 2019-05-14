import cv2
import zmq
import base64
from picamera.array import PiRGBArray
from picamera import PiCamera
import time

class clientStreamer(object):
    ''' clientStreamer '''

    def __init__(self):

        self.footage_socket = zmq.Context().socket(zmq.PUB)
        self.messaging_socket = zmq.Context().socket(zmq.SUB)
        # continue with this messaging socket to receive and print messages
        # as a test. other end on lightsail
        
        self.camera = ""
        self.rawCapture = ""
        #self.footage_socket.connect('tcp://localhost:5050')    # local testing
        print "Port initialized and waiting on connection...\n"

    def connect_streaming_socket(self, ip, port):
        connection_address = 'tcp://' + ip + ':' + port
        #self.footage_socket.connect('tcp://18.214.123.134:5050')
        self.footage_socket.connect(connection_address)
        
    def start_camera(self):
        print "Initializing camera..."
        self.camera = PiCamera()
        self.camera.resolution = (640, 480)
        self.camera.framerate = 32
        self.rawCapture = PiRGBArray(self.camera, size=(640, 480))
        time.sleep(0.1)    # Warm up camera
        print "Camera initialized."
    
    def begin_stream(self):
        print "beginning stream... "
        
        test_bool = False
        for frame in self.camera.capture_continuous(self.rawCapture, format="bgr",
                                               use_video_port=True):
            if test_bool == False:
                print "connection? "
                test_bool = True
            try:
                image = frame.array
                encoded, buffer = cv2.imencode('.jpg', image)
                jpg_as_text = base64.b64encode(buffer)
                self.footage_socket.send(jpg_as_text)
                self.rawCapture.truncate(0)
                
            except KeyboardInterrupt:
                self.camera.release()
                cv2.destroyAllWindows()
                break


