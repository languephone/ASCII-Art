import cv2
import pygame
import sys

# TODO: Calculate crop area dynamically
# TODO: Deal with gap in text rows

class AsciiVideo:
    """Overall class to run the ascii video program."""

    def __init__(self):
        """Define variables and initialize the game."""
        
        # Window size
        self.win_width = 1152

        # Fonts
        self.font_size = 10

        # Colours
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255) 
        
        # Debug Flag
        self.DEBUG = False

        # Ascii characters
        ascii_range = """$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,"^`'.                            """
        self.ascii_reverse = list(ascii_range)
        self.ascii_reverse.reverse()

        # 8-bit (256) greyscale range to ascii range conversion factor
        self.division_factor = 256 / len(self.ascii_reverse)

        # Create cv2 webcam capture object
        self.capture = cv2.VideoCapture(0)

        # Get sample frame size for window size definition
        img_width = self.capture.get(cv2.CAP_PROP_FRAME_WIDTH)
        img_height = self.capture.get(cv2.CAP_PROP_FRAME_HEIGHT)
        img_ratio = img_height / img_width
        self.win_height = int(self.win_width * img_ratio)
        self.frame_rate = self.capture.get(cv2.CAP_PROP_FPS)

        # Setup Pygame
        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((self.win_width, self.win_height))
        pygame.display.set_caption('Ascii Art')
        self._create_font_object()

        self._calc_pixel_size()


    def _create_font_object(self):
        """Generate pypgame font object used to render text on screen."""
        self.font = pygame.font.SysFont('couriernew', self.font_size)


    def _calc_pixel_size(self):
        """Use window size and font size to calculate chars needed."""
        
        # Calculate size in pixels of chars based on font
        line_width, self.line_height  = self.font.size('#' * 20)
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
        # Reduce pixels for processing
        small = cv2.resize(gray, (self.h_chars, self.v_chars),
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
                sys.exit()
            # Check for pressed keys
            elif event.type == pygame.KEYDOWN:
                self.check_keydown_events(event)


    def check_keydown_events(self, event):
        if event.key == pygame.K_UP:
            if len(self.ascii_reverse) > 71:
                self.change_contrast(-1)
        elif event.key == pygame.K_DOWN:
            if len(self.ascii_reverse) < 100:
                self.change_contrast(1)
        elif event.key == pygame.K_LEFT:
            # Limit min size to 6
            if self.font_size > 6:
                self.change_font_size(-1)
        elif event.key == pygame.K_RIGHT:
            # Limit max size to 24
            if self.font_size < 24:
                self.change_font_size(1)


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


    def run_game(self):
        while True:

            self.check_events()

            # Capture video and resize
            ret, frame = self.capture.read()

            flipped = self._resize_image(frame)
            # cropped = small[60:480, 250:710]

            # Fill screen with black on each frame to overwrite previous frame
            self.screen.fill(self.BLACK)
            
            for index, row in enumerate(flipped):
                
                if self.DEBUG:
                    row_text = self.font.render(print_columns_test(row), False, self.WHITE)
                    row_text = self.font.render(str(index), False, self.WHITE)
                    pygame.draw.line(screen, (0, 255, 255), (0, index * self.line_height),
                                   (self.win_width, index * self.line_height))

                # Create text to show on screen
                row_text = self.font.render(
                                self.convert_to_ascii(row), False, self.WHITE)

                # increment y position of each text row by the line height of the font
                self.screen.blit(row_text, (0, index * self.line_height))


            pygame.display.flip()
            self.clock.tick(self.frame_rate)


if __name__ == '__main__':
    av = AsciiVideo()
    av.run_game()