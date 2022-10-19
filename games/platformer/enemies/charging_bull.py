from base.engines import CollisionsEngine
from base.game_movement import GameMovement
from base.important_variables import screen_length, screen_height
from base.quadratic_equations import PhysicsPath
from base.velocity_calculator import VelocityCalculator
from games.platformer.enemies.enemy import Enemy


class ChargingBull(Enemy):
    """An enemy that charges at players if it sees it"""

    # Modifiable Numbers
    length = VelocityCalculator.get_measurement(screen_length, 8)
    height = VelocityCalculator.get_measurement(screen_height, 10)
    time_to_get_to_max_velocity = 1
    max_velocity = VelocityCalculator.get_velocity(screen_length, 900)

    acceleration_path = None
    current_velocity = 0
    is_charging = False

    def __init__(self, damage, hit_points, platform):
        """Initializes the object"""

        super().__init__(damage, hit_points, platform, "games/platformer/images/charging_bull.png")
        self.number_set_dimensions(platform.right_edge - self.length,
                                   platform.top_edge - self.height, self.length, self.height)

        self.acceleration_path = PhysicsPath()
        self.acceleration_path.set_acceleration_with_velocity(self.time_to_get_to_max_velocity, self.max_velocity)
        self.is_moving_right = False

    def run(self):
        """Runs all the code for the charging bull"""

        GameMovement.run_acceleration(self, self.is_charging, self.acceleration_path)

        charging_bull_distance = VelocityCalculator.calculate_distance(self.current_velocity)
        self.left_edge += charging_bull_distance if self.is_moving_right else -charging_bull_distance

    def run_player_interactions(self, players):
        """Runs the interaction between the ChargingBull and the players (should charge if one gets close)"""

        for player in players:
            distance = self.left_edge - player.right_edge
            distance_needed = VelocityCalculator.get_measurement(screen_length, 45)
            should_charge = distance <= distance_needed and CollisionsEngine.is_vertical_collision(player, self)

            if should_charge:
                self.is_charging = True

    def run_inanimate_object_collision(self, inanimate_object, index_of_sub_component, time):
        """Runs the collision for an inanimate object"""

        is_left_collision = CollisionsEngine.is_left_collision(self, inanimate_object, True, time)
        is_right_collision = CollisionsEngine.is_right_collision(self, inanimate_object, True, time)

        if is_left_collision or is_right_collision:
            self.acceleration_path.current_time = self.time_to_get_to_max_velocity / 2

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


