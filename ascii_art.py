import cv2
import sys
import numpy as np

IMG_WIDTH = 250
IMG_HEIGHT = IMG_WIDTH // 2

img = cv2.imread(sys.argv[1], cv2.IMREAD_GRAYSCALE)
img = cv2.resize(img, (IMG_WIDTH, IMG_HEIGHT), interpolation=cv2.INTER_AREA)

ascii_range = """$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,"^`'. """

ascii_reverse = list(ascii_range)
ascii_reverse.reverse()

# Convert 8-bit (256) colour range to ascii range 
division_factor = 256 / len(ascii_range)

for row in img:
	print(''.join([ascii_reverse[int(pixel / division_factor)]
		for pixel in row]))