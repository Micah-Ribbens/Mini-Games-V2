from math import ceil, floor

from base.events import TimedEvent
from base.important_variables import *
from base.velocity_calculator import VelocityCalculator
from gui_components.component import Component
from base.dimensions import Dimensions
from base.utility_functions import *
from games.bird_shooter.bullet import Bullet
from base.utility_functions import load_and_transform_image


class Player(Component):
    # Player Position
    min_left_edge = 0
    max_left_edge = 0
    min_top_edge = 0
    max_top_edge = 0
    is_facing_right = False
    is_facing_up = False
    vertical_delta = 0
    # Player Components
    path_to_bullet_image = ""
    path_to_player_image = ""
    turret = None
    eye = None
    wait_to_shoot_event = None

    # Size and Velocity
    length = VelocityCalculator.get_measurement(screen_length, 10)
    height = VelocityCalculator.get_measurement(screen_height, 20)
    turret_length = VelocityCalculator.get_measurement(3, screen_length)
    turret_height = VelocityCalculator.get_measurement(3.5, screen_height)
    player_velocity = VelocityCalculator.get_velocity(screen_length, 700)
    turret_velocity = VelocityCalculator.get_velocity(screen_length, 250)
    # Keys
    right_key = None
    left_key = None
    up_key = None
    down_key = None
    shoot_key = None
    move_turret_key = None
    # Miscellaneous
    stun_event = None
    player_number = 1
    new_bullets = []
    cap_extension = ceil(21 / 86 * length)

    def __init__(self, player_keys, player_number, boundaries, is_facing_right):
        super().__init__(f"games/bird_shooter/images/player{player_number}_right.png")
        self.path_to_bullet_image = f"games/bird_shooter/images/player{player_number}_bullet.png"

        self.left_key, self.right_key, self.up_key, self.down_key, self.shoot_key, self.move_turret_key = player_keys

        Dimensions.__init__(self, screen_length / 2, screen_height - self.height, self.length, self.height)

        self.new_bullets = []
        self.wait_to_shoot_event = TimedEvent(.2)
        self.stun_event = TimedEvent(.2)

        self.min_left_edge, self.max_left_edge, self.min_top_edge, self.max_top_edge = boundaries

        self.turret = Component("games/bird_shooter/images/beak.png")
        self.eye = Component("games/bird_shooter/images/enemy_eye.png")

        self.eye.length, self.eye.height = self.eye_size

        self.turret.number_set_dimensions(self.right_edge, self.vertical_midpoint, self.turret_length, self.turret_height)
        self.is_facing_right, self.player_number = is_facing_right, player_number

        transformation_paths = [f"games/bird_shooter/images/player{player_number}_", "games/bird_shooter/images/stunned_"]
        other_paths = [f"games/bird_shooter/images/beak.png", f"games/bird_shooter/images/beak_stunned.png", f"games/bird_shooter/images/enemy_eye.png"]

        for image_path in other_paths:
            load_image(image_path)

        for image_path in transformation_paths:
            load_and_transform_image(image_path)

    def run(self):
        self.new_bullets = []
        self.wait_to_shoot_event.run(self.wait_to_shoot_event.current_time >= self.wait_to_shoot_event.time_needed, False)
        self.stun_event.run(self.stun_event.current_time >= self.stun_event.time_needed, False)

        self.turret.left_edge = self.right_edge - self.cap_extension if self.is_facing_right else self.left_edge - self.turret.length + self.cap_extension
        self.turret.top_edge = self.top_edge + self.vertical_delta

        if self.stun_event.has_finished():
            self.movement()
            self.shoot_bullet()

    def shoot_bullet(self):
        if key_has_been_released(self.shoot_key) and self.wait_to_shoot_event.has_finished():
            self.shoot_laser(get_time_of_key_being_held_in(self.shoot_key))
            self.wait_to_shoot_event.start()

    def movement(self):
        player_distance = VelocityCalculator.calculate_distance(self.player_velocity)
        turret_distance = VelocityCalculator.calculate_distance(self.turret_velocity)

        self.left_edge += player_distance if key_is_pressed(self.right_key) else 0
        self.left_edge -= player_distance if key_is_pressed(self.left_key) else 0

        self.top_edge += player_distance if key_is_pressed(self.down_key) and not key_is_pressed(self.move_turret_key) else 0
        self.top_edge -= player_distance if key_is_pressed(self.up_key) and not key_is_pressed(self.move_turret_key) else 0

        self.left_edge = self.get_new_coordinates(self.min_left_edge, self.max_left_edge, self.left_edge)
        self.top_edge = self.get_new_coordinates(self.min_top_edge, self.max_top_edge, self.top_edge)

        self.vertical_delta -= turret_distance if key_is_pressed(self.up_key) and key_is_pressed(self.move_turret_key) else 0
        self.vertical_delta += turret_distance if key_is_pressed(self.down_key) and key_is_pressed(self.move_turret_key) else 0
        self.vertical_delta = self.get_new_coordinates(30/122 * self.height, self.height - self.turret.height, self.vertical_delta)

        self.is_facing_right = True if key_is_pressed(self.right_key) else self.is_facing_right
        self.is_facing_right = False if key_is_pressed(self.left_key) else self.is_facing_right

        self.is_facing_up = True if key_is_pressed(self.up_key) else self.is_facing_up
        self.is_facing_up = False if key_is_pressed(self.down_key) else self.is_facing_up

    def shoot_laser(self, time_held_in):
        size_multipliers = [1, 1.5, 2]
        times_needed_for_size_change = [.5, 1, float("inf")]

        size_multiplier_index = get_index_of_range(times_needed_for_size_change, time_held_in)
        size_multiplier = size_multipliers[size_multiplier_index]

        damage = size_multiplier_index + 1

        bullet_size = size_multiplier * Bullet.length
        turret_left_edge = self.turret.right_edge if self.is_facing_right else self.turret.left_edge - bullet_size

        self.new_bullets.append(Bullet(self.path_to_bullet_image, turret_left_edge, self.turret.vertical_midpoint - bullet_size / 2, self.is_facing_right, damage, size_multiplier))

    def reset(self):
        self.new_bullets = []
        self.wait_to_shoot_event.reset()

    def get_new_coordinates(self, min_coordinate, max_coordinate, current_coordinate):
        current_coordinate = min_coordinate if current_coordinate < min_coordinate else current_coordinate
        current_coordinate = max_coordinate if current_coordinate > max_coordinate else current_coordinate

        return current_coordinate

    def render(self):
        direction = "right.png" if self.is_facing_right else "left.png"
        original_path = f"games/bird_shooter/images/player{self.player_number}_" if self.stun_event.has_finished() else f"games/bird_shooter/images/stunned_"
        self.path_to_image = f"{original_path}{direction}"

        original_turret_path = f"games/bird_shooter/images/beak"
        turret_type = "_stunned.png" if not self.stun_event.has_finished() else ".png"
        self.turret.path_to_image = f"{original_turret_path}{turret_type}"

        # self.eye.left_edge = self.eye_right_position if self.is_facing_right else self.eye_left_position
        # self.eye.top_edge = self.eye_top_position if self.is_facing_up else self.eye_bottom_position

        super().render()
        self.turret.render()
        # self.eye.render()

    def stun(self, stun_time):
        if self.stun_event.has_finished():
            self.stun_event.start()
            self.stun_event.time_needed = stun_time

    # @property
    # def eye_left_position(self):
    #     return floor(self.left_edge + 32/86 * self.length)
    #
    # @property
    # def eye_right_position(self):
    #     return ceil(self.left_edge + 44/86 * self.length)
    #
    # @property
    # def eye_top_position(self):
    #     return floor(self.top_edge + 41/122 * self.height)
    #
    # @property
    # def eye_bottom_position(self):
    #     return ceil(self.top_edge + 48/122 * self.height)
    #
    @property
    def eye_size(self):
        return [ceil(10/86 * self.length), ceil(10/122 * self.height)]
