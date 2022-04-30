import cv2
import pygame
import sys
from ascii_debug import AsciiDebug
from instructions import Instructions

# TODO: Deal with gap in text rows dynamically
# TODO: Display instructions on screen

class AsciiVideo:
    """Overall class to run the ascii video program."""

    def __init__(self):
        """Define variables and initialize the program."""

        # Fonts
        self.font_size = 10
        self.font_name = 'couriernew'
        # Adjustment to deal with blank space at top & bottom of characters
        self.line_height_adjustment = 4

        # Colours
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255) 
        
        # Ascii characters
        self.ascii_sets = ["""$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,"^`'.                            """,
                               "Ñ@#W$9876543210?!abc;:+=-,._            ",
                               "#WX?*:÷×+=-·        "
                            ]
        self.ascii_set = 0
        self.set_ascii_range(0)

        # Create cv2 webcam capture object
        self.capture = cv2.VideoCapture(0)
        
        # Exit program if no camera
        if not self.capture.isOpened():
            sys.exit("No camera detected")

        # Get camera resolution and frame rate to define pixels needed
        self.img_width = int(self.capture.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.img_height = int(self.capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
        img_ratio = self.img_width / self.img_height
        self.frame_rate = self.capture.get(cv2.CAP_PROP_FPS)

        # Setup Pygame
        pygame.init()

        # Get monitor width & height
        monitor_width, monitor_height = pygame.display.get_desktop_sizes()[0]
        
        # Define window height to be 60% of main monitor size
        self.win_height = int(monitor_height * 0.6)

        # Define window width based on image resolution
        # If image ratio is wider than 4:3, crop to 4:3
        if img_ratio > 4 / 3:
            img_ratio = 4 / 3
        self.win_width = int(self.win_height * img_ratio)
        
        # Set window size in pygame, with 200 px for the instructions
        self.screen = pygame.display.set_mode(
            (self.win_width + 200, self.win_height))

        # Define how to crop image to fit window size
        img_adjustment = int(self.img_width / img_ratio)
        self.crop_width = int((self.img_width - img_adjustment) / 2)
        
        pygame.display.set_caption('Ascii Art')
        self.clock = pygame.time.Clock()
        self._create_font_object()
        self._calc_pixel_size()

        # Create program objects
        self.debug = AsciiDebug(self)
        self.instructions = Instructions(self)


    def _create_font_object(self):
        """Generate pypgame font object used to render text on screen."""
        self.font = pygame.font.SysFont(self.font_name, self.font_size)


    def _calc_pixel_size(self):
        """Use window size and font size to calculate chars needed."""
        
        # Calculate size in pixels of chars based on font
        line_width, self.line_height = self.font.size('#' * 20)
        self.line_height -= self.line_height_adjustment
        self.char_width = line_width / 20
        # To test line hight, use chr(9608), which is a full height character

        # Define number of text characters to fit on screen
        self.h_chars = int(self.win_width / self.char_width)
        self.v_chars = int(self.win_height / self.line_height)

        print(f'Font Size: {self.font_size}')
        print(f'Char Width: {self.char_width}, Line Height: {self.line_height}')
        print(f'Horiz. Chars: {self.h_chars}, Vert. Chars: {self.v_chars}')


    def _resize_image(self, image):
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Crop horizontal size to match window ratio
        cropped = gray[:, self.crop_width:self.img_width - self.crop_width]

        # Reduce pixels for processing
        small = cv2.resize(cropped, (self.h_chars, self.v_chars),
                            interpolation = cv2.INTER_AREA)

        # Mirror reverse
        flipped = cv2.flip(small, 1)

        return flipped


    def convert_to_ascii(self, image_row):
        row_text = (''.join([self.ascii_reverse[int(pixel / self.division_factor)]
                                for pixel in image_row]))

        return row_text


    def check_events(self):
        """Respond to keypresses and mouse events."""
        for event in pygame.event.get():
            # Check if game quit
            if event.type == pygame.QUIT:
                self.capture.release()
                sys.exit()
            # Check for pressed keys
            elif event.type == pygame.KEYDOWN:
                self.check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self.check_keyup_events(event)


    def check_keydown_events(self, event):
        if event.key == pygame.K_UP:
            if len(self.ascii_reverse) > len(self.ascii_sets[self.ascii_set]):
                self.change_contrast(-1)
        elif event.key == pygame.K_DOWN:
            if len(self.ascii_reverse) < len(
                    self.ascii_sets[self.ascii_set]) + 10:
                self.change_contrast(1)
        elif event.key == pygame.K_LEFT:
            # Limit min size to 7
            if self.font_size > 7:
                self.change_font_size(-1)
        elif event.key == pygame.K_RIGHT:
            # Limit max size to 22
            if self.font_size < 22:
                self.change_font_size(1)
        elif event.key == pygame.K_a:
            self.set_ascii_range(1)
        elif event.key == pygame.K_d:
            self.debug.status = True


    def check_keyup_events(self, event):
        if event.key == pygame.K_d:
            self.debug.status = False


    def change_font_size(self, factor):
        """Update font size and re-calc char sizes."""

        self.font_size += factor
        self._create_font_object()
        self._calc_pixel_size()


    def change_contrast(self, factor):

        # Use spaces on the end of the 
        if factor < 0:
            self.ascii_reverse.pop(0)
            self.division_factor = 256 / len(self.ascii_reverse)
        elif factor > 0:
            self.ascii_reverse.insert(0, ' ')
            self.division_factor = 256 / len(self.ascii_reverse)

        print(f'New Contrast: {len(self.ascii_reverse)}')


    def set_ascii_range(self, increment):
        
        # Increment range by one
        self.ascii_set += increment
        # Ensure incrementing wraps back around to first of list
        self.ascii_set = self.ascii_set % len(self.ascii_sets)
        print(f'Ascii Range: {self.ascii_set}')
        # Convert to list
        self.ascii_reverse = list(self.ascii_sets[self.ascii_set])
        # Reverse so that brighter pixels go higher in list
        self.ascii_reverse.reverse()

        # 8-bit (256) greyscale range to ascii range conversion factor
        self.division_factor = 256 / len(self.ascii_reverse)


    def render_text(self, text):
        rendered_text = self.font.render(text, False, self.WHITE)

        return rendered_text


    def run_game(self):
        while True:

            self.check_events()

            # Capture video and resize
            ret, frame = self.capture.read()

            flipped = self._resize_image(frame)

            # Fill screen with black on each frame to overwrite previous frame
            self.screen.fill(self.BLACK)

            # Print instructions
            self.instructions.draw_instructions()
            
            for index, row in enumerate(flipped):
                
                if self.debug.status:
                    row_text = self.debug.print_rows_test(str(index), row)
                else:
                    # Define text to show on screen
                    row_text = self.convert_to_ascii(row)

                # Create rendered text
                rendered_text = self.render_text(row_text)

                # increment y position of each text row by the line height of the font
                self.screen.blit(rendered_text, (0, index * self.line_height))


            pygame.display.flip()
            self.clock.tick(self.frame_rate)


if __name__ == '__main__':
    av = AsciiVideo()
    av.run_game()