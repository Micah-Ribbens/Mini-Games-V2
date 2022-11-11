from gui_components.component import Component
from base.velocity_calculator import VelocityCalculator
from base.important_variables import *
from game_dependencies.platformer.platformer_constants import POWERUP_LENGTH, POWERUP_HEIGHT, POWERUP_OBJECT_TYPE


class Powerup(Component):
    """Anything in the game that aids the player in killing enemies (weapons, damage boosts, ammo, etc.)"""

    object_type = POWERUP_OBJECT_TYPE

    length = POWERUP_LENGTH
    height = POWERUP_HEIGHT

    def __init__(self, left_edge, top_edge, path_to_image):
        """Initializes the object"""

        super().__init__(path_to_image)
        self.number_set_dimensions(left_edge, top_edge, self.length, self.height)

    def run_player_collision(self, player):
        """Runs what should happen when the player and the powerup collide"""

        pass

    def update_for_side_scrolling(self, distance):
        """Moves the powerup, so it can update for side scrolling"""

        self.left_edge -= distance
