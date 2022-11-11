from gui_components.component import Component
from base.important_variables import screen_height
from base.velocity_calculator import VelocityCalculator
from gui_components.component import Component
from base.colors import *
from game_dependencies.platformer.platformer_constants import HEALTH_BAR_HEIGHT


class HealthBar(Component):
    """A health bar for a game character"""

    game_character = None
    default_height = HEALTH_BAR_HEIGHT
    height = default_height
    health_remaining_bar = None
    health_gone_bar = None
    set_size_function = None
    is_addable = False

    def __init__(self, game_character, set_size_function=None):
        """Initializes the object"""

        self.game_character = game_character
        self.health_remaining_bar = Component("")
        self.health_gone_bar = Component("")

        self.health_remaining_bar.color = medium_green
        self.health_gone_bar.color = red

        self.set_size_function = set_size_function if set_size_function is not None else self.default_set_size_function
        self.set_size_function()

    def run(self):
        """Runs all the code necessary for the health bar to work"""

        self.set_size_function()

    def render(self):
        """Renders the health bar onto the screen"""

        # Setting where the bars should be
        length_ratio = self.length / self.game_character.total_hit_points

        self.health_gone_bar.top_edge, self.health_remaining_bar.top_edge = self.top_edge, self.top_edge
        self.health_remaining_bar.height, self.health_gone_bar.height = self.height, self.height
        self.health_remaining_bar.left_edge = self.left_edge

        self.health_remaining_bar.length = length_ratio * self.game_character.hit_points_left
        self.health_gone_bar.left_edge = self.health_remaining_bar.right_edge

        # So there is not a rounding error producing a small part of the health bar being red
        self.health_gone_bar.length = self.length - self.health_remaining_bar.length

        # Rendering
        self.health_remaining_bar.render()

        # Even if the length of it is 0, then it is still being rendered on the screen (a small sliver), so this prevents that
        if self.health_gone_bar.length != 0:
            self.health_gone_bar.render()

    def default_set_size_function(self):
        """Runs the default way to size the health bar"""

        self.height = self.game_character.height * .1
        self.left_edge, self.length = self.game_character.left_edge, self.game_character.length
        self.top_edge = self.game_character.top_edge - self.height




