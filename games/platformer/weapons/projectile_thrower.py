from base.events import TimedEvent
from base.important_variables import screen_height, screen_length
from base.utility_functions import is_within_screen
from base.velocity_calculator import VelocityCalculator
from games.platformer.weapons.weapon import Weapon
from base.engines import CollisionsEngine
from gui_components.component import Component


class Projectile(Component):
    """A projectile that the projectile thrower uses"""

    size = VelocityCalculator.get_measurement(screen_height, 6)
    length, height = size, size
    is_moving_right = False
    velocity = 0
    is_runnable = False
    is_destroyed = False
    index = 0
    total_hit_points = 0
    hit_points_left = 0
    user = None

    def __init__(self, left_edge, top_edge, is_moving_right, user_max_velocity, object_type, total_hit_points, user, path_to_image):
        """Initializes the object"""

        super().__init__(path_to_image)
        self.number_set_dimensions(left_edge, top_edge, self.size, self.size)

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

    # def render(self):
    #     print("RENDER")


class ProjectileThrower(Weapon):
    """A weapon that is used for throwing projectiles"""

    deleted_sub_components_indexes = []

    def __init__(self, use_action, user):
        """Initializes the object"""

        super().__init__(10, 10, use_action, user, .2)
        self.sub_components = []

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

        self.sub_components.append(Projectile(self.get_weapon_left_edge(Projectile.size, self.user.should_shoot_right),
                                   self.user.projectile_top_edge - Projectile.size, self.user.should_shoot_right,
                                   self.user.projectile_velocity, self.object_type, self.total_hit_points, self.user,
                                   "games/platformer/images/player_projectile.png"))

    def run_enemy_collision(self, user, index_of_sub_component):
        """Runs the code for figuring out what to do when one of the projectiles hits an enemy or an enemy's projectile"""

        user.cause_damage(self.damage)
        self.deleted_sub_components_indexes.append(index_of_sub_component)

    def run_inanimate_object_collision(self, inanimate_object, index_of_sub_component, time):
        """Runs all the code for figuring ot what to do when one of the projectiles hits an inanimate object (platforms, trees, etc.)"""

        self.deleted_sub_components_indexes.append(index_of_sub_component)

    def reset(self):
        """Resets everything back to the start of the game"""

        self.sub_components = []



