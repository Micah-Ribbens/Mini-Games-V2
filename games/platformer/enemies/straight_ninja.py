from base.lines import Point
from base.important_variables import screen_length, screen_height
from base.paths import VelocityPath, ActionPath
from base.velocity_calculator import VelocityCalculator
from games.platformer.enemies.enemy import Enemy
from games.platformer.weapons.bouncy_projectile_thrower import BouncyProjectileThrower
from games.platformer.weapons.projectile_thrower import Projectile, ProjectileThrower


class StraightEnemy(Enemy):
    path = None
    velocity = VelocityCalculator.get_velocity(screen_length, 300)
    length = VelocityCalculator.get_measurement(screen_length, 5)
    height = VelocityCalculator.get_measurement(screen_height, 10)
    weapon = None
    is_facing_right = None
    is_gone = None

    # By default the Straight Enemy has this path, but the Bouncy Enemy has a different path
    def __init__(self, damage, hit_points, platform, path_to_image="games/platformer/images/straight_tank.png"):
        """Initializes the object"""

        super().__init__(damage, hit_points, platform, path_to_image)
        self.number_set_dimensions(platform.left_edge, platform.top_edge - self.height, self.length, self.height)

        top_edge = platform.top_edge - self.height
        wait_time = .5
        # Creating the path for the ninja
        self.path = ActionPath(Point(platform.right_edge - self.length, top_edge), self, self.velocity)
        self.path.add_point(Point(platform.left_edge, top_edge), lambda: [])
        self.path.add_point(Point(platform.left_edge, top_edge), self.shoot_star, wait_time)
        self.path.add_point(Point(platform.right_edge - self.length, top_edge), lambda: [])
        self.path.add_point(Point(platform.right_edge - self.length, top_edge), self.shoot_star, wait_time)

        self.path.is_unending = True
        self.weapon = ProjectileThrower(lambda: False, self)

    def hit_player(self, player, index_of_sub_component):
        pass

    def hit_by_player(self, player_weapon, index_of_sub_component):
        pass

    def run(self):
        """Runs everything necessary in order for this enemy to work"""

        self.sub_components = [self] + self.weapon.get_sub_components()

        self.components = self.sub_components + [self.health_bar]
        self.path.run()
        self.weapon.run()

    def shoot_star(self):
        """Shoots a star"""

        # Casting to int prevents a rounding error (off by .000000001 or less)
        self.is_facing_right = int(self.left_edge) == int(self.platform.left_edge)

        # Sometimes there is a bad lag spike, so the enemy won't stop meaning then I have to check if the enemy
        # Is now moving right (slope of the x coordinate line is increasing means the x coordinates are increasing)
        if int(self.left_edge) != int(self.platform.left_edge) and int(self.right_edge) != int(self.platform.right_edge):
            self.is_facing_right = self.path.x_coordinate_lines[self.path.get_index_of_line(self.path.total_time)].slope_is_positive()

        self.weapon.run_upon_activation()

    @property
    def projectile_velocity(self):
        return self.velocity



