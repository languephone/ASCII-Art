import cv2
import pygame
import sys

# Image Size
HEIGHT = int(1080 / 10)
WIDTH = int(1920 / 10)

# Colors
BLACK = (0, 0, 0)
GRAY = (180, 180, 180)
WHITE = (255, 255, 255)

# Fonts
FONT_SIZE = 9

ascii_range = """$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,"^`'. """
ascii_reverse = list(ascii_range)
ascii_reverse.reverse()

# Convert 8-bit (256) colour range to ascii range 
division_factor = 256 / len(ascii_range)

capture = cv2.VideoCapture(0)

def convert_to_ascii(image_row):
    row_text = (''.join([ascii_reverse[int(pixel / division_factor)]
                for pixel in row]))

    return row_text


def update_screen():
    screen.fill(BLACK)
    screen.blit(ascii_text)

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((800, 800))
pygame.display.set_caption("Ascii Art")
smallFont = pygame.font.SysFont('sfnsmono', FONT_SIZE)

while True:
    
    # Check if game quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    ret, frame = capture.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    small = cv2.resize(gray, (WIDTH, HEIGHT))
    # cropped = small[60:480, 250:710]

    screen.fill(BLACK)
    
    for index, row in enumerate(small):
        row_text = smallFont.render(convert_to_ascii(row), False, WHITE)
        screen.blit(row_text, (0, index * FONT_SIZE))

    pygame.display.flip()