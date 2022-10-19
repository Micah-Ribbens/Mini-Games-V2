from gui_components.component import Component
from base.velocity_calculator import VelocityCalculator
from base.dimensions import Dimensions
from base.important_variables import *


class Laser(Component):
    velocity = VelocityCalculator.get_velocity(screen_height, 500)
    height = VelocityCalculator.get_measurement(screen_height, 9)
    length = VelocityCalculator.get_measurement(screen_length, 4)
    damage = 0

    def __init__(self, horizontal_midpoint, bottom_edge, path_to_image, size_multiplier, damage):
        self.length = self.length * size_multiplier
        self.height = self.height * size_multiplier
        self.damage, self.path_to_image = damage, path_to_image

        top_edge = bottom_edge - self.height
        left_edge = horizontal_midpoint - self.length / 2
        super().__init__(path_to_image)

        Dimensions.__init__(self, left_edge, top_edge, self.length, self.height)

    def run(self):
        self.top_edge -= VelocityCalculator.calculate_distance(self.velocity)


