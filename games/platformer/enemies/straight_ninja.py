from base.lines import Point
from base.important_variables import screen_length, screen_height
from base.paths import VelocityPath, ActionPath
from base.velocity_calculator import VelocityCalculator
from games.platformer.enemies.enemy import Enemy
from games.platformer.weapons.bouncy_projectile_thrower import BouncyProjectileThrower
from games.platformer.weapons.straight_projectile_thrower import StraightProjectile, StraightProjectileThrower


class StraightEnemy(Enemy):
    action_path = None
    velocity = VelocityCalculator.get_velocity(screen_length, 300)
    length = VelocityCalculator.get_measurement(screen_length, 5)
    height = VelocityCalculator.get_measurement(screen_height, 10)
    weapon = None
    is_facing_right = None
    is_gone = None

    # By default the Straight Enemy has this action_path, but the Bouncy Enemy has a different action_path
    def __init__(self, damage, hit_points, platform, base_image_path="games/platformer/images/straight_tank"):
        """Initializes the object"""

        super().__init__(damage, hit_points, platform, base_image_path)
        self.number_set_dimensions(platform.left_edge, platform.top_edge - self.height, self.length, self.height)

        top_edge = platform.top_edge - self.height
        wait_time = .5
        # Creating the action_path for the ninja
        self.action_path = ActionPath(Point(platform.right_edge - self.length, top_edge), self, self.velocity)
        self.action_path.add_point(Point(platform.left_edge, top_edge), lambda: [])
        self.action_path.add_point(Point(platform.left_edge, top_edge), self.shoot_star, wait_time)
        self.action_path.add_point(Point(platform.right_edge - self.length, top_edge), lambda: [])
        self.action_path.add_point(Point(platform.right_edge - self.length, top_edge), self.shoot_star, wait_time)

        self.action_path.is_unending = True
        self.weapon = StraightProjectileThrower(lambda: False, self)
        self.weapon.has_limited_ammo = False

    def update_for_side_scrolling(self, amount):
        """Updates the enemy after side scrolling,so nothing funky happens (like being on an invisible platform)"""

        self.action_path.update_for_side_scrolling(amount)
        self.weapon.update_for_side_scrolling(amount)
        # super().update_for_side_scrolling(amount)

    def hit_player(self, player, index_of_sub_component):
        pass

    def hit_by_player(self, player_weapon, index_of_sub_component):
        pass

    def run(self):
        """Runs everything necessary in order for this enemy to work"""

        self.sub_components = [self] + self.weapon.get_sub_components()

        self.components = self.sub_components + [self.health_bar]
        self.action_path.run()
        self.weapon.run()

    def shoot_star(self):
        """Shoots a star"""

        self.is_facing_right = not self.is_facing_right

        self.weapon.run_upon_activation()

    @property
    def projectile_velocity(self):
        return self.velocity



