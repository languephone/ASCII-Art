import pygame.font

class Instructions:
	"""A class to show instructions on screen."""

	def __init__(self, av_object):
		"""Initialize instructions attributes."""
		
		self.av_object = av_object

		# Font settings for scoring information.
		self.text_color = (255, 255, 255)
		self.font = pygame.font.SysFont('Impact', 18)

		font_size_text = "Change font size"
		contrast_text = "Use up/down arrows to change contrast."
		ascii_set_text = "Press 'a' key to cycle between different fonts"
		debug_text = "Hold 'd' key to enable debug mode."

		instruction_list = [font_size_text, contrast_text, ascii_set_text,
			debug_text]

		self.instruction_images = [self.prep_text(text) for text
			in instruction_list]
		print(self.instruction_images)

	def prep_text(self, text):
		"""Turn the text into a rendered image for display."""

		text_image = self.font.render(text, True, self.text_color)

		return text_image


	def draw_instructions(self):
		"""Turn the text into a rendered image for display."""

		self.av_object.screen.blit(self.instruction_images[0],
			(self.av_object.win_width, 0))