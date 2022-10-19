from math import ceil, floor

from base.important_variables import screen_length, screen_height
from base.velocity_calculator import VelocityCalculator
from gui_components.component import Component
from base.utility_functions import load_and_transform_image


class Enemy(Component):
    # Movement and Direction
    base_velocity = VelocityCalculator.get_velocity(screen_length, 70)
    velocity = base_velocity
    velocity_increase = velocity * .2
    total_hits_to_change_direction = 5
    hits_left_to_change_direction = total_hits_to_change_direction
    is_moving_right = False
    is_moving_down = True
    # Size and Eyes
    length = VelocityCalculator.get_measurement(screen_length, 11)
    height = length
    left_eye = Component("games/bird_shooter/images/enemy_eye.png")
    right_eye = Component("games/bird_shooter/images/enemy_eye.png")

    def __init__(self):
        super().__init__("")
        load_and_transform_image("games/bird_shooter/images/enemy_")
        self.center()

        self.left_eye.length, self.left_eye.height = self.eye_size
        self.right_eye.length, self.right_eye.height = self.eye_size

    def run(self):
        self.path_to_image = "games/bird_shooter/images/enemy_right.png" if self.is_moving_right else "games/bird_shooter/images/enemy_left.png"

        if self.hits_left_to_change_direction <= 0:
            self.hits_left_to_change_direction = self.total_hits_to_change_direction
            self.is_moving_right = not self.is_moving_right
            self.velocity += self.velocity_increase

        distance = VelocityCalculator.calculate_distance(self.velocity)

        self.top_edge += distance if self.is_moving_down else -distance
        self.left_edge += distance if self.is_moving_right else -distance

        if self.top_edge <= 0:
            self.top_edge = 0
            self.is_moving_down = True

        if self.bottom_edge >= screen_height:
            self.top_edge = screen_height - self.height
            self.is_moving_down = False

        self.left_eye.left_edge, self.right_eye.left_edge = self.eye_right_positions if self.is_moving_right else self.eye_left_positions
        self.left_eye.top_edge, self.right_eye.top_edge = self.eye_bottom_edge_positions if self.is_moving_down else self.eye_top_positions

    def center(self):
        self.left_edge = (screen_length / 2) - (self.length / 2)
        self.top_edge = (screen_height / 2) - (self.height / 2)

    def render(self):
        super().render()
        self.left_eye.render()
        self.right_eye.render()

    def reset(self):
        self.center()
        self.velocity = self.base_velocity

    @property
    def eye_size(self):
        return [4/47 * self.length, 4/47 * self.height]

    @property
    def eye_left_positions(self):
        return [floor(self.left_edge + 12 / 47 * self.length) - 1, floor(self.left_edge + 30 / 47 * self.length) - 1]

    @property
    def eye_right_positions(self):
        return [ceil(self.left_edge + 14/47 * self.length) + 1, ceil(self.left_edge + 32/47 * self.length) + 1]

    @property
    def eye_top_positions(self):
        return [floor(self.top_edge + 18 / 47 * self.height) - 1] * 2

    @property
    def eye_bottom_edge_positions(self):
        return [ceil(self.top_edge + 20/47 * self.height) + 1] * 2


