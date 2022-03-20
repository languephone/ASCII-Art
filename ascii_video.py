import cv2
# import pygame
# import numpy as np

SCALE = 0.6
HEIGHT = int(1080 / 2)
WIDTH = int(1920 / 2)

ascii_range = """$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,"^`'. """
ascii_reverse = list(ascii_range)
ascii_reverse.reverse()

# Convert 8-bit (256) colour range to ascii range 
division_factor = 256 / len(ascii_range)

capture = cv2.VideoCapture(0)

def convert_to_ascii(image):
    for row in img:
        print(''.join([ascii_reverse[int(pixel / division_factor)]
              for pixel in row]))

while True:
    ret, frame = capture.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    small = cv2.resize(gray, (WIDTH, HEIGHT))
     
    cv2.imshow('webcam', small[60:480, 250:710])
     
    if cv2.waitKey(1) == 27:
        break

capture.release()
cv2.destroyAllWindows()