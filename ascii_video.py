import cv2
import pygame
import sys

# TODO: Calculate screen size and crop area dynamically
# TODO: Deal with gap in text rows

# Window Size
WIN_WIDTH = 1100
WIN_HEIGHT = 900

# Fonts
FONT_SIZE = 11

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Debug Flat
DEBUG = False

def resize_image(image):
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Reduce pixels for processing
    small = cv2.resize(gray, (h_chars, v_chars),
                        interpolation = cv2.INTER_AREA)
    # Mirror reverse
    flipped = cv2.flip(small, 1)

    return flipped


def convert_to_ascii(image_row):
    row_text = (''.join([ascii_reverse[int(pixel / division_factor)]
                for pixel in image_row]))

    return row_text


def print_columns_test(row):
    # Define numbers 1 to 10 to repeat
    char_bank = [i for i in range(10)]
    # Replace last character with . to easily see end of column
    char_bank[-1] = '.'
    # Define characters to print as list
    col_list = [char_bank[i % 10] for i in range(len(row))]
    # Join characters into single string
    col_text = (''.join([str(i) for i in row_list]))

    return col_text


def print_rows_test(index, row):
    # Define characters to print as list
    row_list = [index for i in range(len(row))]
    # Join characters into single string
    row_text = (''.join([index for i in row_list]))

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
    global ascii_range, ascii_reverse, division_factor
    if event.key == pygame.K_UP:
        ascii_range += " "
        ascii_reverse = list(ascii_range)
        ascii_reverse.reverse()
    elif event.key == pygame.K_DOWN:
        if ascii_reverse[0] == " ":
            ascii_reverse = ascii_reverse[1:]


def update_screen():
    screen.fill(BLACK)
    screen.blit(ascii_text)


# Define variables
ascii_range = """$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,"^`'.                            """
ascii_reverse = list(ascii_range)
ascii_reverse.reverse()

# 8-bit (256) greyscale range to ascii range conversion factor
division_factor = 256 / len(ascii_reverse)

# Create cv2 webcam capture object
capture = cv2.VideoCapture(0)

# Setup Pygame
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Ascii Art")
font = pygame.font.SysFont('couriernew', FONT_SIZE)

# Calculate size in pixels of chars based on font
line_width, line_height  = font.size('#' * 10)
char_width = line_width / 10
# To test line hight, use chr(9608), which is a full height character

# Get sample frame size for resizing
ret, frame = capture.read()
img_width = len(frame)
img_height = len(frame[0])
img_ratio = img_width / img_height

# Define number of text characters to fit on screen
h_chars = int(WIN_WIDTH / char_width)
v_chars = int(WIN_HEIGHT / line_height)

print(f'char width: {char_width}, line height: {line_height}')
print(f'horiz. chars: {h_chars}, vert. chars: {v_chars}')

while True:

    check_events()

    # Capture video and resize
    ret, frame = capture.read()

    
    flipped = resize_image(frame)
    # cropped = small[60:480, 250:710]

    # Fill screen with black on each frame to overwrite previous frame
    screen.fill(BLACK)
    
    for index, row in enumerate(flipped):
        
        if DEBUG:
            row_text = font.render(print_columns_test(row), False, WHITE)
            row_text = font.render(str(index), False, WHITE)
            pygame.draw.line(screen, (0, 255, 255), (0, index * line_height),
                           (WIN_WIDTH, index * line_height))

        # Create text to 
        row_text = font.render(convert_to_ascii(row), False, WHITE)

        # increment y position of each text row by the # of pixels in the font
        screen.blit(row_text, (0, index * line_height))


    pygame.display.flip()
    clock.tick(60)