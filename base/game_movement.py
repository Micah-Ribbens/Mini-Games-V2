import pygame.key

from base.important_variables import screen_height, screen_length
from base.utility_functions import key_is_pressed
from base.velocity_calculator import VelocityCalculator


class GameMovement:
    """A class that gives helper methods for movement in a game"""

    @staticmethod
    def set_player_vertical_movement(player, max_top_edge, min_top_edge):
        """Sets the player's movement and y coordinates so it stays within these bounds"""

        player.can_move_down = False if player.bottom_edge >= max_top_edge else True
        player.can_move_up = False if player.top_edge <= min_top_edge else True

        if player.top_edge <= min_top_edge:
            player.top_edge = min_top_edge

        if player.bottom_edge >= max_top_edge:
            player.top_edge = max_top_edge - player.height

    @staticmethod
    def set_player_horizontal_movement(player, max_left_edge, min_left_edge):
        """Sets the player's movement and x coordinates so it stays within these bounds"""

        player.can_move_right = False if player.right_edge >= max_left_edge else True
        player.can_move_left = False if player.left_edge <= min_left_edge else True

        if player.right_edge >= max_left_edge:
            player.left_edge = max_left_edge - player.length

        if player.left_edge <= min_left_edge:
            player.left_edge = min_left_edge

    @staticmethod
    def player_horizontal_movement(player, player_velocity, left_key, right_key):
        """Runs the player's horizontal movement"""

        if player.can_move_left and key_is_pressed(left_key):
            player.left_edge -= VelocityCalculator.calculate_distance(player_velocity)

        if player.can_move_right and key_is_pressed(right_key) and not key_is_pressed(left_key):
            player.left_edge += VelocityCalculator.calculate_distance(player_velocity)

    @staticmethod
    def player_vertical_movement(player, player_velocity, up_key, down_key, can_move_up=None, can_move_down=None):
        """Runs the player's vertical movement"""

        can_move_up = player.can_move_up if can_move_up is None else can_move_up
        can_move_down = player.can_move_down if can_move_down is None else can_move_down

        if key_is_pressed(up_key) and can_move_up:
            player.top_edge -= VelocityCalculator.calculate_distance(player_velocity)

        if key_is_pressed(down_key) and can_move_down:
            player.top_edge += VelocityCalculator.calculate_distance(player_velocity)

    @staticmethod
    def run_projectile_movement(projectile, forwards_velocity, upwards_velocity):
        """Runs the movement for a projectile that moves horizontally and vertically"""

        horizontal_distance = VelocityCalculator.calculate_distance(forwards_velocity)
        vertical_distance = VelocityCalculator.calculate_distance(upwards_velocity)

        projectile.left_edge += horizontal_distance if projectile.is_moving_right else -horizontal_distance
        projectile.top_edge += vertical_distance if projectile.is_moving_down else -vertical_distance

        if projectile.bottom_edge >= screen_height:
            distance_change = projectile.bottom_edge - screen_height
            projectile.is_moving_down = False
            projectile.top_edge = screen_height - distance_change - projectile.height

        if projectile.top_edge <= 0:
            distance_change = -projectile.top_edge
            projectile.top_edge = projectile.top_edge + distance_change
            projectile.is_moving_down = True

    @staticmethod
    def run_acceleration(player, should_accelerate, acceleration_path, player_max_velocity):
        """Runs the acceleration of the player: player must have the attributes: 'current_velocity'"""

        acceleration_path.run(False, should_accelerate, True)
        player.current_velocity = acceleration_path.get_final_velocity()

        if player.current_velocity > player_max_velocity:
            player.current_velocity = player_max_velocity


