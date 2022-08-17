import cv2
import pygame
import sys
import os
import sound_effects as se
from debug import AsciiDebug, FramesPerSecond
from interface import Instructions, Separator, Button, UiElement, DialogueBox
from camera import Camera

# TODO: Deal with gap in text rows dynamically
# TODO: Show font size and contrast info on screen in debug window instead of terminal
# TODO: Prevent screen grabs saving over previous screen grabs

class AsciiVideo:
    """Overall class to run the ascii video program."""

    def __init__(self):
        """Define variables and initialize the program."""

        # Fonts
        self.font_size = 10
        self.font_name = 'couriernew'
        # Adjustment to deal with blank space at top & bottom of characters
        self.line_height_adjustment = 2

        # Colours
        self.BLACK = (25, 25, 25)
        self.WHITE = (255, 255, 255) 
        
        # Ascii characters
        self.ascii_sets = [
            """$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,"^`'.                            """,
            "Ñ@#W$9876543210?!abc;:+=-,._            ",
            "#WX?*:÷×+=-·        "
        ]
        self.ascii_set = 0
        self.prep_ascii_range()

        self.camera = Camera()
        
        # Setup Pygame
        pygame.init()
        pygame.display.set_caption('Ascii Art')
        self.clock = pygame.time.Clock()

        # Get monitor width & height
        monitor_width, monitor_height = pygame.display.get_desktop_sizes()[0]
        
        # Define window height to be 60% of main monitor size
        self.win_height = int(monitor_height * 0.6)

        # Define window width based on image resolution
        # If image ratio is wider than 4:3, crop to 4:3
        if self.camera.img_ratio > 3 / 3:
            self.camera.img_ratio = 3 / 3
        self.win_width = int(self.win_height * self.camera.img_ratio)

        # Set window size in pygame, with 300 px for the UI
        self.screen = pygame.display.set_mode(
            (self.win_width + 300, self.win_height))

        # Define how to crop image to fit window size
        img_adjustment = int(self.camera.img_height * self.camera.img_ratio)
        self.crop_width = int((self.camera.img_width - img_adjustment) / 2)

        # Create program objects
        self._create_font_object()
        self._calc_pixel_size()
        self.debug = AsciiDebug(self)
        self.ui_elements = UiElement(self)
        self.dialogue_box = DialogueBox(self)
        self.fps = FramesPerSecond(self)


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


    def _resize_image(self, image):
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Crop horizontal size to match window ratio
        horizontal_slice = slice(self.crop_width,
            self.camera.img_width - self.crop_width)
        cropped = gray[:, horizontal_slice]

        # Reduce pixels for processing
        small = cv2.resize(cropped, (self.h_chars, self.v_chars),
                            interpolation = cv2.INTER_AREA)

        # Mirror reverse
        flipped = cv2.flip(small, 1)

        return flipped


    def convert_to_ascii(self, image_row):
        row_text = (''.join([self.ascii_reverse[int(pixel / 
            self.division_factor)] for pixel in image_row]))

        return row_text


    def check_events(self):
        """Respond to keypresses and mouse events."""
        for event in pygame.event.get():
            # Check if game quit
            if event.type == pygame.QUIT:
                self.camera.capture.release()
                sys.exit()
            # Check for pressed keys
            elif event.type == pygame.KEYDOWN:
                self.check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self.check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self.check_button_events(mouse_pos)
            elif event.type == pygame.MOUSEBUTTONUP:
                # Revert colour of buttons back to normal
                for button in self.ui_elements.buttons:
                    button.button_color = (100, 100, 100)
                    button._prep_msg()


    def check_keydown_events(self, event):
        """Respond to keypresses."""
        if event.key == pygame.K_UP:
            self.change_contrast(-1)
        elif event.key == pygame.K_DOWN:
            self.change_contrast(1)
        elif event.key == pygame.K_LEFT:
            self.change_font_size(-1)
        elif event.key == pygame.K_RIGHT:
            self.change_font_size(1)
        elif event.key == pygame.K_a:
            self.set_ascii_range(1)
        elif event.key == pygame.K_d:
            self.debug.status = True


    def check_keyup_events(self, event):
        """Respond to key releases."""
        if event.key == pygame.K_d:
            self.debug.status = False


    def check_button_events(self, mouse_pos):
        """Respond to mouse buttons"""
        for button in self.ui_elements.buttons:
            if button.rect.collidepoint(mouse_pos):
                # Change colour of button
                button.button_color = (150, 150, 150)
                button._prep_msg()
                if button.msg == 'Decrease Font':
                    self.change_font_size(-1)
                    se.decrease_button.play()
                if button.msg == 'Increase Font':
                    self.change_font_size(1)
                    se.increase_button.play()
                if button.msg == 'Decrease Contrast':
                    self.change_contrast(-1)
                    se.decrease_button.play()
                if button.msg == 'Increase Contrast':
                    self.change_contrast(1)
                    se.increase_button.play()
                if button.msg == 'Previous Set':
                    self.update_ascii_range(1)
                    se.decrease_button.play()
                if button.msg == 'Next Set':
                    self.update_ascii_range(-1)
                    se.increase_button.play()
                if button.msg == 'Image Only':
                    self.save_screen_portion()
                    se.decrease_button.play()
                if button.msg == 'Whole Window':
                    self.save_screen_image()
                    se.increase_button.play()
                if button.msg == 'Debug':
                    self.debug.toggle_status()
                    se.decrease_button.play()
                if button.msg == 'Toggle FPS':
                    self.fps.toggle_status()
                    se.increase_button.play()


    def change_font_size(self, factor):
        """Update font size and re-calc char sizes."""
        # Limit font size range to between 7pt and 22pt
        if self.font_size > 7 and factor < 0\
            or self.font_size < 22 and factor > 0:
            self.font_size += factor
            self._create_font_object()
            self._calc_pixel_size()
            self.dialogue_box.set_message(f'Font size: {self.font_size}')
            self.dialogue_box.set_display_time()

            if self.debug.status:
                print(f'Font Size: {self.font_size}')
                print(f'Char Width: {self.char_width}, Line Height: {self.line_height}')
                print(f'Horiz. Chars: {self.h_chars}, Vert. Chars: {self.v_chars}')


    def change_contrast(self, factor):
        """Increase or decrease trailing spaces in ASCII char set."""
        # Limit addition/removal of space characters
        if factor < 0:
            if len(self.ascii_reverse) > len(self.ascii_sets[self.ascii_set]):
                self.ascii_reverse.pop(0)
                self.division_factor = 256 / len(self.ascii_reverse)
        elif factor > 0:
            if len(self.ascii_reverse) < len(
                    self.ascii_sets[self.ascii_set]) + 10:
                self.ascii_reverse.insert(0, ' ')
                self.division_factor = 256 / len(self.ascii_reverse)
        self.dialogue_box.set_message(f'Contrast: {len(self.ascii_reverse)}')
        self.dialogue_box.set_display_time()


    def prep_ascii_range(self):
        """Reset characteristics based on different character sets."""

        # Convert to list
        self.ascii_reverse = list(self.ascii_sets[self.ascii_set])
        # Reverse so that brighter pixels go higher in list
        self.ascii_reverse.reverse()

        # 8-bit (256) greyscale range to ascii range conversion factor
        self.division_factor = 256 / len(self.ascii_reverse)

    
    def update_ascii_range(self, increment):
        """Change to next set in list and re-calc reversal."""
        self.ascii_set += increment
        # Ensure incrementing wraps back around to first of list
        self.ascii_set = self.ascii_set % len(self.ascii_sets)
        self.prep_ascii_range()
        self.dialogue_box.set_message(f'Ascii set: {self.ascii_set + 1}')
        self.dialogue_box.set_display_time()


    def save_screen_text(self):
        with open('saved_images/screen_shot.txt', 'w') as f:
            ret, frame = self.camera.capture.read()
            flipped = self._resize_image(frame)

            for row in flipped:
                f.write(self.convert_to_ascii(row) + '\n')


    def save_screen_image(self):
        """Save image file of entire pygame screen."""
        if not os.path.exists('saved_images'):
            os.mkdir('saved_images')
        pygame.image.save(self.screen, 'saved_images/screenshot.png')
        self.dialogue_box.set_message("Screenshot Saved")
        self.dialogue_box.set_display_time()


    def save_screen_portion(self):
        """Save image file of video portion of pygame screen."""
        if not os.path.exists('saved_images'):
            os.mkdir('saved_images')
        portion = self.screen.subsurface(0, 0, self.win_width,
            self.win_height)
        pygame.image.save(portion, 'saved_images/screenshot.png')
        self.dialogue_box.set_message("Screenshot Saved")
        self.dialogue_box.set_display_time()


    def run_game(self):
        while True:

            self.check_events()

            # Capture video and resize
            ret, frame = self.camera.capture.read()

            flipped = self._resize_image(frame)

            # Fill screen with black on each frame to overwrite previous frame
            self.screen.fill(self.BLACK)

            # Display UI
            for instruction in self.ui_elements.instructions:
                instruction.draw_instructions()
            for separator in self.ui_elements.separators:
                separator.draw_single_line()
            for button in self.ui_elements.buttons:
                button.draw_button()
            if self.fps.status:
                self.fps.display_fps()

            # Display ASCII text
            for index, row in enumerate(flipped):
                
                if self.debug.status:
                    if index == self.v_chars // 2:
                        row_text = self.debug.print_columns_test(row)
                    else:
                        row_text = self.debug.print_rows_test(index, row)

                else:
                    # Define text to show on screen
                    row_text = self.convert_to_ascii(row)

                # Create rendered text
                rendered_text = self.font.render(row_text, False, self.WHITE,
                    self.BLACK)

                # increment y position of each text row by the line height of the font
                self.screen.blit(rendered_text, (0, index * self.line_height))

            # Display dialogue boxes
            if self.dialogue_box.time_left > pygame.time.get_ticks():
                self.dialogue_box.draw_dialogue()

            pygame.display.flip()
            self.clock.tick(self.camera.frame_rate)


if __name__ == '__main__':
    av = AsciiVideo()
    av.run_game()