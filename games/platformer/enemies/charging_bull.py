from base.engines import CollisionsEngine
from base.game_movement import GameMovement
from base.history_keeper import HistoryKeeper
from base.important_variables import screen_length, screen_height
from base.quadratic_equations import PhysicsPath
from base.velocity_calculator import VelocityCalculator
from games.platformer.enemies.enemy import Enemy
from game_dependencies.platformer.platformer_constants import *


class ChargingBull(Enemy):
    """An enemy that charges at players if it sees it"""

    # Modifiable Numbers
    length = CHARGING_BULL_LENGTH
    height = CHARGING_BULL_HEIGHT

    acceleration_path = None
    current_velocity = 0
    is_charging = False

    def __init__(self, damage, hit_points, platform):
        """Initializes the object"""

        super().__init__(damage, hit_points, platform, "games/platformer/images/charging_bull")
        self.number_set_dimensions(platform.right_edge - self.length,
                                   platform.top_edge - self.height, self.length, self.height)

        self.acceleration_path = PhysicsPath()
        self.acceleration_path.set_acceleration_with_velocity(CHARGING_BULL_TIME_TO_MAX_HORIZONTAL_VELOCITY, CHARGING_BULL_MAX_HORIZONTAL_VELOCITY)
        self.is_moving_right = False

    def run(self):
        """Runs all the code for the charging bull"""

        GameMovement.run_acceleration(self, self.is_charging, self.acceleration_path, CHARGING_BULL_MAX_HORIZONTAL_VELOCITY)

        charging_bull_distance = VelocityCalculator.calculate_distance(self.current_velocity)

        # If it is in the air, then it should not go as fast
        if not self.is_on_platform:
            charging_bull_distance /= CHARGING_BULL_DECREASE_MULTIPLAYER_WHEN_IN_AIR

        self.left_edge += charging_bull_distance if self.is_moving_right else -charging_bull_distance

        # If the HistoryKeeper has no data on this object then it is impossible to see if there are any collisions with it
        if HistoryKeeper.get_last(self.name) is not None:
            self.update_is_on_platform()

    def run_player_interactions(self, players):
        """Runs the interaction between the ChargingBull and the players (should charge if one gets close)"""

        for player in players:
            distance = self.left_edge - player.right_edge
            should_charge = distance <= CHARGING_BULL_DISTANCE_NEEDED_TO_CHARGE and CollisionsEngine.is_vertical_collision(player, self)

            if should_charge:
                self.is_charging = True

    def run_inanimate_object_collision(self, inanimate_object, index_of_sub_component):
        """Runs the collision for an inanimate object"""

        is_left_collision = CollisionsEngine.is_left_collision(self, inanimate_object, True)
        is_right_collision = CollisionsEngine.is_right_collision(self, inanimate_object, True)
        is_horizontal_collision = is_left_collision or is_right_collision

        if is_horizontal_collision:
            self.run_horizontal_inanimate_object_collision(inanimate_object, is_left_collision, is_right_collision)

        # If it is not a horizontal collision, then it must be the top collision
        if not is_horizontal_collision:
            self.update_top_collision_data(inanimate_object)

    def run_horizontal_inanimate_object_collision(self, inanimate_object, is_left_collision, is_right_collision):
        """Runs the horizontal direction of inanimate object collisions"""

        self.acceleration_path.current_time = CHARGING_BULL_TIME_TO_MAX_HORIZONTAL_VELOCITY / 2

        if is_left_collision:
            self.is_moving_right = False
            self.left_edge = inanimate_object.left_edge - self.length

        elif is_right_collision:
            self.is_moving_right = True
            self.left_edge = inanimate_object.right_edge

    def hit_player(self, player, index_of_sub_component):
        pass

    def hit_by_player(self, player_weapon, index_of_sub_component):
        pass



