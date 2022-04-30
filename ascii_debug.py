class AsciiDebug:
     """Class to manage debugging."""

     def __init__(self, av_object):
          """Initialize the debugging tools."""

          self.status = False
          self.axis = 0


     def print_columns_test(self, row):
         """Print a repeated row of numbers 1-10 to visually confirm the length
               of a row."""

         # Define numbers 1 to 10 to repeat
         char_bank = [i for i in range(10)]
         # Replace last character with . to easily see end of column
         char_bank[-1] = '.'
         # Define characters to print as list
         col_list = [char_bank[i % 10] for i in range(len(row))]
         # Join characters into single string
         col_text = (''.join([str(i) for i in row_list]))

         return col_text


     def print_rows_test(self, index, row):
         # Define characters to print as list
         row_list = [index for i in range(len(row))]
         # Join characters into single string
         row_text = (' '.join([index for i in row_list]))

         return row_text


     def run_debug_columns(self, row):
          
          self.row_text = av_object.font.render(
               self.print_columns_test(row), False, av_object.WHITE)

     def run_debug_rows(self, axis):

          if self.axis == 0:
               self.row_text = av_object.font.render(
                    self.print_rows_test(index, row), False, av_object.WHITE)
     
          pygame.draw.line(av_object.screen, (0, 255, 255),
               (0, index * av_object.line_height),
               (av_object.win_width, index * av_object.line_height))
