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
		contrast_text = "Change contrast."
		ascii_set_text = "Cycle between character sets"
		debug_text = "Hold to enable debug mode."

		interface_list = [font_size_text, contrast_text, ascii_set_text,
			debug_text]

		self.interface_images = [self.prep_text(text) for text
			in interface_list]

		self.text_distance = av_object.win_height / len(interface_list)


	def prep_text(self, text):
		"""Turn the text into a rendered image for display."""

		text_image = self.font.render(text, True, self.text_color)

		return text_image


	def draw_interface(self):
		"""Turn the text into a rendered image for display."""

		for index, image in enumerate(self.interface_images):
			self.av_object.screen.blit(image,
				(self.av_object.win_width + 5, self.text_distance * index))