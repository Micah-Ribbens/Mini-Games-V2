from base.dimensions import Dimensions
from base.history_keeper import HistoryKeeper
from base.important_variables import game_window
from base.utility_functions import *
from base.velocity_calculator import VelocityCalculator


class Component(Dimensions):
    color = None
    path_to_image = None
    last_cycle_time_when_visible = 0
    name = ""
    is_addable = True
    is_runnable = True  # Sometimes the screen has to run the player, so some components shouldn't be run

    def __init__(self, path_to_image=""):
        self.path_to_image = path_to_image

        if path_to_image != "":
            load_image(path_to_image)

        self.name = id(self)

    def run(self):
        pass

    def render(self):
        if self.path_to_image != "":
            render_image(self.path_to_image, self.left_edge, self.top_edge, self.length, self.height)

        else:
            render_rectangle(self.left_edge, self.top_edge, self.length, self.height, self.color)

        self.last_cycle_time_when_visible = VelocityCalculator.time

    def got_clicked(self):
        was_visible_last_cycle = self.last_cycle_time_when_visible == HistoryKeeper.last_time
        return mouse_is_clicked() and is_mouse_collision(self) and was_visible_last_cycle