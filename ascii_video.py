import cv2
import pygame
import sys

# TODO: Calculate screen size and crop area dynamically
# TODO: Understand font size vertical & horizontal pixels

# Image Size
VSCALE = 0.07
HSCALE = 0.1

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Fonts
FONT_SIZE = 9

ascii_range = """$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,"^`'.                         """
ascii_reverse = list(ascii_range)
ascii_reverse.reverse()

# Convert 8-bit (256) colour range to ascii range 
division_factor = 256 / len(ascii_range)

capture = cv2.VideoCapture(0)

def resize_image(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    small = cv2.resize(gray, None, fx=HSCALE, fy=VSCALE,
                       interpolation = cv2.INTER_AREA)

    return small


def convert_to_ascii(image_row):
    row_text = (''.join([ascii_reverse[int(pixel / division_factor)]
                for pixel in row]))

    return row_text


def check_events():
    for event in pygame.event.get():
        # Check if game quit
        if event.type == pygame.QUIT:
            sys.exit()
        # Check for pressed keys
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event)


def check_keydown_events(event):
    if event.key == pygame.K_UP:
        print('up key')
    elif event.key == pygame.K_DOWN:
        print('down key')


def update_screen():
    screen.fill(BLACK)
    screen.blit(ascii_text)


# Initialize Pygame
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((1100, 750))
pygame.display.set_caption("Ascii Art")
smallFont = pygame.font.SysFont('couriernew', FONT_SIZE)

while True:

    for event in pygame.event.get():
        # Check if game quit
        if event.type == pygame.QUIT:
            sys.exit()

    check_events()

    # Capture video and resize
    ret, frame = capture.read()

    small = resize_image(frame)
    flipped = cv2.flip(small, 1)
    # cropped = small[60:480, 250:710]

    # Render ascii_text
    screen.fill(BLACK)
    
    for index, row in enumerate(flipped):
        row_text = smallFont.render(convert_to_ascii(row), False, WHITE)
        row_rect = row_text.get_rect()
        pygame.draw.rect(screen, WHITE, pygame.Rect(row_rect))
        # increment y position of each text row by the # of pixels in the font
        screen.blit(row_text, (0, index * (FONT_SIZE - 1)))

    pygame.display.flip()
    clock.tick(30)