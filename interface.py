import pygame.font

class Instructions:
	"""A class to show user instructions on screen."""

	def __init__(self, av_object):
		"""Initialize instructions attributes."""
		
		self.av_object = av_object
		self.win_width = av_object.win_width
		self.win_height = av_object.win_height

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

		self.text_distance = self.win_height / len(instruction_list)


	def prep_text(self, text):
		"""Turn the text into a rendered image for display."""

		text_image = self.font.render(text, True, self.text_color)

		return text_image


	def draw_instructions(self):
		"""Turn the text into a rendered image for display."""

		for index, image in enumerate(self.instruction_images):
			self.av_object.screen.blit(image,
				(self.win_width + 5, self.text_distance * index))


class Interface:
	"""A class to show UI elements."""

	def __init__(self, av_object):
		"""Initialize interface attributes."""

		self.av_object = av_object
		self.win_width = av_object.win_width
		self.win_height = av_object.win_height

		self.instructions = Instructions(av_object)
		self.text_distance = self.win_height / len(
			self.instructions.instruction_images)

	def draw_separation_lines(self):

		for index, image in enumerate(self.instructions.instruction_images):

			# Draw a separation line
			pygame.draw.line(self.av_object.screen, (100, 100, 100),
				start_pos=(self.win_width + 5, self.text_distance * index + 23),
				end_pos=(self.win_width + 275, self.text_distance * index + 23))

class Button:
	"""A class to create UI buttons."""

	def __init__(self, av_object, msg, h_pos, v_pos):
		"""Initialize button attributes."""
		self.av_object = av_object
		self.win_width = av_object.win_width
		self.win_height = av_object.win_height

		# Set the dimensions and properties of the button.
		self.width, self.height = 100, 30
		self.button_color = (100, 100, 100)
		self.text_color = (200, 200, 200)
		self.font = pygame.font.SysFont('helveticaneue', 12)

		# Build the button's rect object and center it.
		self.rect = pygame.Rect(h_pos, v_pos, self.width, self.height)

		# Prep the button message.
		self._prep_msg(msg)


	def _prep_msg(self, msg):
		"""Turn msg into rendered image and center text on button."""
		self.msg_img = self.font.render(msg, True, self.text_color,
										self.button_color)
		self.msg_img_rect = self.msg_img.get_rect()
		self.msg_img_rect.center = self.rect.center


	def draw_button(self):
		"""Draw a blank button and then draw message."""
		# self.av_object.screen.fill(self.button_color, self.rect)
		pygame.draw.rect(self.av_object.screen, self.button_color, self.rect,
			border_radius=4)
		self.av_object.screen.blit(self.msg_img, self.msg_img_rect)
