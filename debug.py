import pygame.font

class AsciiDebug:
     """Class to manage debugging."""

     def __init__(self, av_object):
          """Initialize the debugging tools."""

          self.status = False
          self.av_object = av_object

     def print_columns_test(self, row):
          """
          Print a repeated row of numbers 1-10 to visually confirm the length
          of a row.
          """

          # Define numbers 1 to 10 to repeat
          char_bank = [i for i in range(1, 10)]
          # Make last character '.' to easily see end of column
          char_bank.append('.')
          # Define characters to print as list
          col_list = [char_bank[i % 10] for i in range(len(row))]
          # Join characters into single string
          return ''.join([str(i) for i in col_list])

     def print_rows_test(self, index, row):
          """
          Print column of numbers to visually confirm the number
          of horizontal rows on screen.
          """
         
          # Use row length to only print characters in middle of screen
          return str(index).center(self.av_object.h_chars)

     def toggle_status(self):
          if self.status:
               self.status = False
          else:
               self.status = True


class FramesPerSecond:
     """A class to manage the fps display."""
     def __init__(self, av_object):
          """Initialize fps attributes."""
          self.font = pygame.font.SysFont('helveticaneue', 10)
          self.text_color = (0, 255, 0) # Bright green
          self.background_color = av_object.BLACK
          self.h_pos = av_object.win_width + 8
          self.v_pos = av_object.win_height - 16
          self.screen = av_object.screen
          self.clock = av_object.clock
          self.status = False

     def display_fps(self):

          fps = 'FPS:' + str(int(self.clock.get_fps()))
          fps_text = self.font.render(fps, True, self.text_color,
               self.background_color)
          self.screen.blit(fps_text, (self.h_pos, self.v_pos))

     def toggle_status(self):
          # Fill screen portion with black to cover up text
          self.screen.fill(self.background_color, (self.h_pos, self.v_pos,
               self.width, self.height))
          
          if self.status:
               self.status = False
          else:
               self.status = True