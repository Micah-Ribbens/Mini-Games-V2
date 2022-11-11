from base.paths import ActionPath
from game_dependencies.platformer.platformer_constants import *
from games.platformer.enemies.enemy import Enemy
from games.platformer.weapons.straight_projectile_thrower import StraightProjectileThrower


class StraightEnemy(Enemy):
    action_path = None
    length = STRAIGHT_ENEMY_LENGTH
    height = STRAIGHT_ENEMY_HEIGHT
    weapon = None
    is_facing_right = None
    is_gone = None

    # By default the Straight Enemy has this action_path, but the Bouncy Enemy has a different action_path
    def __init__(self, damage, hit_points, platform, base_image_path="games/platformer/images/straight_tank"):
        """Initializes the object"""

        super().__init__(damage, hit_points, platform, base_image_path)
        self.number_set_dimensions(platform.left_edge, platform.top_edge - self.height, self.length, self.height)

        top_edge = platform.top_edge - self.height
        # Creating the action_path for the ninja
        self.action_path = ActionPath(Point(platform.right_edge - self.length, top_edge), self, STRAIGHT_ENEMY_HORIZONTAL_VELOCITY)
        self.action_path.add_point(Point(platform.left_edge, top_edge), lambda: [])
        self.action_path.add_point(Point(platform.left_edge, top_edge), self.shoot_star, STRAIGHT_ENEMY_ACTION_PATH_WAIT_TIME)
        self.action_path.add_point(Point(platform.right_edge - self.length, top_edge), lambda: [])
        self.action_path.add_point(Point(platform.right_edge - self.length, top_edge), self.shoot_star, STRAIGHT_ENEMY_ACTION_PATH_WAIT_TIME)

        self.action_path.is_unending = True
        self.weapon = StraightProjectileThrower(lambda: False, self, STRAIGHT_ENEMY_HORIZONTAL_VELOCITY)
        self.weapon.has_limited_ammo = False

    def update_for_side_scrolling(self, amount):
        """Updates the enemy after side scrolling,so nothing funky happens (like being on an invisible platform)"""

        self.action_path.update_for_side_scrolling(amount)
        self.weapon.update_for_side_scrolling(amount)

    def hit_player(self, player, index_of_sub_component):
        pass

    def hit_by_player(self, player_weapon, index_of_sub_component):
        pass

    def run(self):
        """Runs everything necessary in order for this enemy to work"""

        self.action_path.run()
        self.weapon.run()

    def shoot_star(self):
        """Shoots a star"""

        self.is_facing_right = not self.is_facing_right

        self.weapon.run_upon_activation()

    @property
    def projectile_velocity(self):
        return STRAIGHT_ENEMY_HORIZONTAL_VELOCITY

    def get_components(self):
        """returns: Component[]; all the components of the straight enemy that should be rendered and ran"""

        return [self] + self.weapon.get_collidable_components() + [self.health_bar]



