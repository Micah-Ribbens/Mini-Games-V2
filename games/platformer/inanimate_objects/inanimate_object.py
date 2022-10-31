from base.important_variables import (
    screen_height,
    screen_length,
)

from base.velocity_calculator import VelocityCalculator
from gui_components.component import Component


class InanimateObject(Component):
    """The platform that the players can jump onto and interact with"""

    color = (150, 75, 0)
    object_type = "Platform"

    def __init__(self, path_to_image):
        """Initializes the object"""

        super().__init__(path_to_image)

    def update_for_side_scrolling(self, amount):
        """Updates the inanimate object, so it side scrolls"""

        self.left_edge -= amount

