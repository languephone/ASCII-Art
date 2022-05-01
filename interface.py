import pygame.font

class Interface:
	"""A class to show interface on screen."""

	def __init__(self, av_object):
		"""Initialize interface attributes."""
		
		self.av_object = av_object

		# Font settings for scoring information.
		self.text_color = (255, 255, 255)
		self.font = pygame.font.SysFont('Impact', 18)

		font_size_text = "Change font size"
		contrast_text = "Use up/down arrows to change contrast."
		ascii_set_text = "Press 'a' key to cycle between different fonts"
		debug_text = "Hold 'd' key to enable debug mode."

		interface_list = [font_size_text, contrast_text, ascii_set_text,
			debug_text]

		self.interface_images = [self.prep_text(text) for text
			in interface_list]
		print(self.interface_images)

	def prep_text(self, text):
		"""Turn the text into a rendered image for display."""

		text_image = self.font.render(text, True, self.text_color)

		return text_image


	def draw_interface(self):
		"""Turn the text into a rendered image for display."""

		self.av_object.screen.blit(self.interface_images[0],
			(self.av_object.win_width, 0))