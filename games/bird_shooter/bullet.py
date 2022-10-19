from base.velocity_calculator import VelocityCalculator
from base.important_variables import *
from gui_components.component import Component


class Bullet(Component):
    length = VelocityCalculator.get_measurement(screen_length, 2)
    height = length
    velocity = VelocityCalculator.get_velocity(screen_height, 700)
    total_hits_to_destroy = 0
    hits_left_to_destroy = 0
    damage = 0
    size_multiplier = 0
    is_moving_right = True

    def __init__(self, path_to_image, left_edge, top_edge, is_moving_right, damage, size_multiplier):
        super().__init__(path_to_image)
        self.left_edge, self.top_edge = left_edge, top_edge
        self.is_moving_right = is_moving_right
        self.damage, self.size_multiplier = damage, size_multiplier
        self.hits_left_to_destroy, self.total_hits_to_destroy = damage, damage

        self.length *= size_multiplier
        self.height *= size_multiplier

    def run(self):
        distance = VelocityCalculator.calculate_distance(self.velocity)
        self.left_edge += distance if self.is_moving_right else -distance