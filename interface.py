import pygame.font

class Instructions:
    """A class to show user instructions on screen."""

    def __init__(self, av_object, msg, v_pos):
        """Initialize instructions attributes."""

        self.av_object = av_object
        self.msg = msg
        self.v_pos = v_pos
        self.win_width = av_object.win_width

        # Font settings for instructions.
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont('helveticaneue', 18)

        # Create image from text
        self.instruction_image = self.prep_text()


    def prep_text(self):
        """Turn the text into a rendered image for display."""

        text_image = self.font.render(self.msg, True, self.text_color)

        return text_image


    def draw_instructions(self):
        """Display rendered image on screen."""

        self.av_object.screen.blit(self.instruction_image,
            (self.win_width + 5, self.v_pos))


class Separator:
    """A class to show decorative UI elements."""

    def __init__(self, av_object, v_pos):
        """Initialize interface attributes."""

        self.av_object = av_object
        self.win_width = av_object.win_width
        self.v_pos = v_pos


    def draw_single_line(self):

        pygame.draw.line(self.av_object.screen, (100, 100, 100),
            start_pos=(self.win_width + 5, self.v_pos + 23),
            end_pos=(self.win_width + 275, self.v_pos + 23))


class Button:
    """A class to create UI buttons."""

    def __init__(self, av_object, msg, h_index, v_pos):
        """Initialize button attributes."""
        self.av_object = av_object
        self.msg = msg

        # Set the dimensions and properties of the button.
        self.width, self.height = 100, 25
        self.button_color = (100, 100, 100)
        self.text_color = (200, 200, 200)
        self.font = pygame.font.SysFont('helveticaneue', 12)

        self.h_pos = self.av_object.win_width + (self.width * h_index) + (5 * h_index) + 5

        # Build the button's rect object and center it.
        self.rect = pygame.Rect(self.h_pos, v_pos + 30, self.width, self.height)

        # Prep the button message.
        self._prep_msg()


    def _prep_msg(self):
        """Turn msg into rendered image and center text on button."""
        self.msg_img = self.font.render(self.msg, True, self.text_color,
                                        self.button_color)
        self.msg_img_rect = self.msg_img.get_rect()
        self.msg_img_rect.center = self.rect.center


    def draw_button(self):
        """Draw a blank button and then draw message."""

        pygame.draw.rect(self.av_object.screen, self.button_color, self.rect,
            border_radius=4)
        self.av_object.screen.blit(self.msg_img, self.msg_img_rect)


class DialogueBox:
    """A class to display messages to the user."""
    def __init__(self, av_object):
        """Initialize dialog box attributes."""
        self.av_object = av_object

        # Set the dimensions and properties of the box.
        self.width = int(self.av_object.win_width * 0.7)
        self.height = int(self.av_object.win_height * 0.2)
        self.button_color = (100, 100, 100)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont('helveticaneue', 40)
        self.h_pos = int(self.av_object.win_width * 0.15)
        self.v_pos = int(self.av_object.win_height * 0.3)

        # Set display time
        self.display_time = 1500 # milliseconds
        self.time_left = 0

        # Build the button's rect object and center it.
        self.rect = pygame.Rect(0, 0, self.width, self.height)

    def set_message(self, message):
        self.msg = message
        self._prep_msg()
        self._create_transparent_surface()

    def _prep_msg(self):
        """Turn msg into rendered image and center text on button."""
        self.msg_img = self.font.render(self.msg, True, self.text_color,
                                        self.button_color)
        self.msg_img_rect = self.msg_img.get_rect()
        self.msg_img_rect.center = self.rect.center

    def _create_transparent_surface(self):
        """Create transparant surfact to place box and text."""
        self.trans_surf = pygame.Surface((self.width, self.height))
        self.trans_surf.set_alpha(230) # 0-255 scale
        # Draw gray rectangle onto transparent surface
        pygame.draw.rect(self.trans_surf, self.button_color, self.rect,
            border_radius=4)
        # Blit message onto transparent surface
        self.trans_surf.blit(self.msg_img, self.msg_img_rect)

    def set_display_time(self):
        """Define expiration time for dialogue box."""
        self.time_left = pygame.time.get_ticks() + self.display_time

    def draw_dialogue(self):
        """Blit transparent surface onto display surface."""
        self.av_object.screen.blit(self.trans_surf, (self.h_pos, self.v_pos))



class UiElement:
    """A class to create a complete UI element."""

    def __init__(self, av_object):
        """Initialize element attributes."""

        self.av_object = av_object

        self.elements = [
            {'text': 'Change font size',
                'buttons': ['Decrease Font', 'Increase Font']},
            {'text': 'Change contrast',
                'buttons': ['Decrease Contrast', 'Increase Contrast']},
            {'text': 'Cycle between character sets',
                'buttons': ['Previous Set', 'Next Set']},
            {'text': 'Take screen shot',
                 'buttons': ['Image Only', 'Whole Window']},
            {'text': 'Debug mode',
                 'buttons': ['Debug', 'Toggle FPS']}
        ]

        # Define vertical position of each element based on number of elements
        self.v_spacing = self.av_object.win_height / len(self.elements)

        # Generate all required UI objects and put into lists
        self.instructions = []
        self.separators = []
        self.buttons = []

        for index, element in enumerate(self.elements):

            instruction, separator, button_list = self.create_ui_element(
                element['text'], element['buttons'], index)

            self.instructions.append(instruction)
            self.separators.append(separator)
            self.buttons.extend(button_list)


    def create_ui_element(self, inst_msg, buttons, index):
        """Create each individual UI element for UI section."""

        v_pos = self.v_spacing * index

        instruction = Instructions(self.av_object, inst_msg, v_pos)
        separator = Separator(self.av_object, v_pos)

        # Create list of button objects
        button_list = []
        for h_index, button in enumerate(buttons):
            button_list.append(Button(self.av_object, button, h_index, v_pos))

        return instruction, separator, button_list