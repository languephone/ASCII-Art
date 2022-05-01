import cv2
import sys
import numpy as np

class AsciiPhoto():
    """Overall class to manage static photo conversion to Ascii."""

    def __init__(self):

        # Read image and convert to grayscale
        self.img = cv2.imread(sys.argv[1], cv2.IMREAD_GRAYSCALE)
        
        # Calculate output width & height
        self.img_width, self.img_height = self.img.shape
        img_ratio = self.img_width / self.img_height
        self.output_width = 60
        self.output_height = int(self.output_width / img_ratio)

        # Define adjustment needed for black space between rows
        self.line_height_adjustment = 2

        self.output_height = int(self.output_height / self.line_height_adjustment)

        # Resize image to match required output size
        self.img = cv2.resize(self.img,
            (self.output_width , self.output_height),
            interpolation=cv2.INTER_AREA)

        self.ascii_range = """$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,"^`'.           """

        self.ascii_reverse = list(self.ascii_range)
        self.ascii_reverse.reverse()

        # Convert 8-bit (256) greyscale range to ascii range 
        self.division_factor = 256 / len(self.ascii_range)


    def print_to_file(self):
        
        # Print to text file
        output_name = sys.argv[1].split('/')[-1]
        output_name = output_name.split('.')[0] + '.txt'

        with open(output_name, 'w') as f:
            for row in self.img:
                f.write(''.join(
                    [self.ascii_range[int(pixel / self.division_factor)
                        ] for pixel in row]) + '\n')


    def print_to_terminal(self):
        # Show in terminal
        for row in self.img:
            print(''.join([self.ascii_reverse[int(pixel / self.division_factor)]
                for pixel in row]))


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


photo = AsciiPhoto()
photo.print_to_terminal()
photo.print_to_file()