import cv2
import sys
import time

class Camera:
    def __init__(self):
        # Create cv2 webcam capture object
        self.capture = cv2.VideoCapture(0)

        # Exit program if no camera
        if not self.capture.isOpened():
            sys.exit("No camera detected")

        # Get camera resolution and frame rate to define pixels needed
        self.img_width = int(self.capture.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.img_height = int(self.capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.img_ratio = self.img_width / self.img_height
        self.get_frame_rate()

    def get_frame_rate(self):
        num_frames = 60

        start = time.time()

        for i in range(num_frames):
            ret, frame = self.capture.read()

        end = time.time()
        seconds = end - start
        self.frame_rate = num_frames / seconds
