import pygame.font

class Instructions:
	"""A class to show user instructions on screen."""

	def __init__(self, av_object):
		"""Initialize instructions attributes."""
		
		self.av_object = av_object

		# Font settings for scoring information.
		self.text_color = (255, 255, 255)
		self.font = pygame.font.SysFont('helveticaneue', 18)

		font_size_text = "Change font size"
		contrast_text = "Change contrast."
		ascii_set_text = "Cycle between character sets"
		debug_text = "Hold to enable debug mode."

		instruction_list = [font_size_text, contrast_text, ascii_set_text,
			debug_text]

		self.instruction_images = [self.prep_text(text) for text
			in instruction_list]

		self.text_distance = self.av_object.win_height / len(instruction_list)


	def prep_text(self, text):
		"""Turn the text into a rendered image for display."""

		text_image = self.font.render(text, True, self.text_color)

		return text_image


	def draw_instructions(self):
		"""Turn the text into a rendered image for display."""

		for index, image in enumerate(self.instruction_images):
			self.av_object.screen.blit(image,
				(self.av_object.win_width + 5, self.text_distance * index))


class Interface:
	"""A class to show UI elements."""

	def __init__(self, av_object):
		"""Initialize interface attributes."""

		self.av_object = av_object
		self.instructions = Instructions(av_object)
		self.text_distance = self.av_object.win_height / len(
			self.instructions.instruction_images)

	def draw_separation_lines(self):

		for index, image in enumerate(self.instructions.instruction_images):

			# Draw a separation line
			pygame.draw.line(self.av_object.screen, (220, 220, 220),
				start_pos=(self.av_object.win_width + 5, self.text_distance *
					index), end_pos=(self.av_object.win_width + 300,
					self.text_distance * index ))

