from base.utility_functions import render_image
from gui_components.component import Component
from base.important_variables import *
from base.utility_functions import *


class Screen(Component):
    components = []
    path_to_background_file = ""
    is_visible = True

    def __init__(self, path_to_background_file):
        self.path_to_background_file = path_to_background_file

        if self.path_to_background_file != "":
            load_image(path_to_background_file)

    def get_components(self):
        return self.components

    def render_background(self):
        if self.path_to_background_file != "":
            render_image(self.path_to_background_file, 0, 0, screen_length, screen_height)

    def run_on_close(self):
        pass