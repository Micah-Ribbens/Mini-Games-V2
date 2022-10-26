from base.dimensions import Dimensions
from base.important_variables import game_window
from gui_components.component import Component
from base.utility_functions import *

class TextBox(Component):
    text = ""
    font = None
    font_size = 0
    background_color = None
    text_color = None
    is_centered = False

    def __init__(self, text, font_size, background_color, text_color, is_centered):
        if not isinstance(text, str):
            raise ValueError("Text must be a string")

        self.text, self.font_size = text, font_size
        self.text_color, self.is_centered = text_color, is_centered
        self.background_color, self.color = background_color, background_color
        load_text(id(self), font_size, background_color, text_color)
        super().__init__("")
        Dimensions.__init__(self, 0, 0, 0, 0)

    def render(self):
        super().render()

        left_edge, top_edge = self.left_edge, self.top_edge

        if self.is_centered:
            left_edge, top_edge = self.horizontal_midpoint, self.vertical_midpoint

        render_text(left_edge, top_edge, self.text_color, self.background_color, self.text, self.font_size, self.is_centered, id(self))

    def set_background_color(self, background_color):
        self.color, self.background_color = background_color, background_color

