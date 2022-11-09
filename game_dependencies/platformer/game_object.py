from base.important_variables import (
    screen_height,
    screen_length,
)

from base.velocity_calculator import VelocityCalculator
from gui_components.component import Component


class GameObject:
    """A class that use is for providing functions and attributes that must be in common for all game objects (or at least almost all)"""

    object_type = ""

    def update_for_side_scrolling(self, amount):
        """Updates the inanimate object, so it side scrolls"""

        self.left_edge -= amount

