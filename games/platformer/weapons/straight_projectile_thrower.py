from base.events import TimedEvent
from base.important_variables import screen_height, screen_length
from base.utility_functions import is_within_screen
from base.velocity_calculator import VelocityCalculator
from games.platformer.weapons.weapon import Weapon
from base.engines import CollisionsEngine
from gui_components.component import Component
from base.utility_functions import load_and_transform_image, get_direction_path_to_image
from game_dependencies.platformer.platformer_constants import *


class StraightProjectile(Component):
    """A projectile that the projectile thrower uses"""

    length = STRAIGHT_PROJECTILE_LENGTH
    height = STRAIGHT_PROJECTILE_HEIGHT
    is_moving_right = False
    velocity = 0
    is_runnable = False
    is_destroyed = False
    index = 0
    total_hit_points = 0
    hit_points_left = 0
    user = None
    base_path_to_image = ""

    def __init__(self, left_edge, top_edge, is_moving_right, user_max_velocity, object_type, total_hit_points, user, base_path_to_image):
        """Initializes the object"""

        self.base_path_to_image = base_path_to_image
        load_and_transform_image(base_path_to_image)
        super().__init__(f"{base_path_to_image}_right.png")

        self.number_set_dimensions(left_edge, top_edge, self.length, self.height)

        self.total_hit_points, self.hit_points_left = total_hit_points, total_hit_points
        self.is_moving_right = is_moving_right
        self.velocity = user_max_velocity + VelocityCalculator.get_measurement(screen_height, 50)
        self.object_type, self.user = object_type, user

    def run(self):
        """Runs all the code for the projectile to move across the screen and other necessary things"""

        distance = VelocityCalculator.calculate_distance(self.velocity)
        self.left_edge += distance if self.is_moving_right else -distance

    def cause_damage(self, amount):
        """Causes damage to the projectile"""

        self.hit_points_left -= amount

    def render(self):
        """Renders the projectile onto the screen"""

        self.path_to_image = get_direction_path_to_image(self.base_path_to_image, self.is_moving_right, "")
        super().render()


class StraightProjectileThrower(Weapon):
    """A weapon that is used for throwing projectiles"""

    deleted_sub_components_indexes = []
    user_type = ""  # Stores the information for loading in images (either an enemy or player projectile)
    weapon_name = STRAIGHT_THROWER_WEAPON_NAME
    user_max_velocity = 0

    def __init__(self, use_action, user, user_max_velocity):
        """Initializes the object"""

        self.user_max_velocity = user_max_velocity
        super().__init__(STRAIGHT_THROWER_WEAPON_DAMAGE, STRAIGHT_THROWER_WEAPON_HIT_POINTS, use_action, user, STRAIGHT_THROWER_COOL_DOWN_TIME)
        self.sub_components = []
        self.user_type = "enemy" if user.object_type == "Enemy" else "player"

    def run(self):
        """Runs all the code necessary in order for this object to work"""

        super().run()
        # TODO maybe consider updating this if the game is running slow
        updated_sub_components = []

        # This for loop updates the sub_components, so all the ones that should be deleted are because they are not
        # Added to updated_sub_components; also all the subcomponents are run
        for x in range(len(self.sub_components)):
            projectile = self.sub_components[x]

            should_be_deleted = not is_within_screen(projectile) or projectile.hit_points_left <= 0

            if not should_be_deleted and not self.deleted_sub_components_indexes.__contains__(x):
                projectile.run()
                projectile.index = len(updated_sub_components) + self.user.weapon_index_offset
                updated_sub_components.append(projectile)

        self.sub_components = updated_sub_components
        self.deleted_sub_components_indexes = []

    def run_upon_activation(self):
        """Runs the code that should be completed when the code decides to use this weapon"""

        if self.ammo_left > 0 or not self.has_limited_ammo:
            self.sub_components.append(StraightProjectile(self.get_weapon_left_edge(StraightProjectile.length, self.user.should_shoot_right),
                                       self.user.projectile_top_edge - StraightProjectile.height, self.user.should_shoot_right,
                                       self.user_max_velocity, self.object_type, self.total_hit_points, self.user,
                                       f"games/platformer/images/{self.user_type}_projectile"))

            self.ammo_left -= 1

    def run_enemy_collision(self, user, index_of_sub_component):
        """Runs the code for figuring out what to do when one of the projectiles hits an enemy or an enemy's projectile"""

        user.cause_damage(self.damage)
        self.deleted_sub_components_indexes.append(index_of_sub_component)

    def run_inanimate_object_collision(self, inanimate_object, index_of_sub_component, time):
        """Runs all the code for figuring ot what to do when one of the projectiles hits an inanimate object (platforms, trees, etc.)"""

        self.deleted_sub_components_indexes.append(index_of_sub_component)

    def update_for_side_scrolling(self, amount):
        for projectile in self.sub_components:
            projectile.left_edge -= amount

    def reset(self):
        """Resets everything back to the start of the game"""

        self.sub_components = []
        self.ammo_left = BASE_WEAPON_AMMO




