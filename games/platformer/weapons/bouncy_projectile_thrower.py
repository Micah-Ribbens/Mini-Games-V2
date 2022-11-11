from base.engines import CollisionsEngine
from base.important_variables import screen_length, screen_height
from base.quadratic_equations import PhysicsPath
from base.velocity_calculator import VelocityCalculator
from games.platformer.weapons.straight_projectile_thrower import StraightProjectile, StraightProjectileThrower
from game_dependencies.platformer.platformer_constants import *

class BouncyProjectile(StraightProjectile):
    """A projectile that bounces"""

    projectile_path = None
    size = BOUNCY_PROJECTILE_SIZE
    length, height = size, size

    def __init__(self, left_edge, top_edge, is_moving_right, projectile_height, user_velocity, object_type, total_hit_points, user, path_to_image):
        """Initializes the object"""

        super().__init__(left_edge, top_edge, is_moving_right, user_velocity, object_type, total_hit_points, user, path_to_image)
        time_to_vertex = TIME_TO_BOUNCY_PROJECTILE_VERTEX
        self.projectile_path = PhysicsPath(game_object=self, attribute_modifying="top_edge", height_of_path=-projectile_height, initial_distance=top_edge - self.height, time=time_to_vertex)
        self.projectile_path.set_initial_distance(top_edge - self.height)
        self.projectile_path.current_time = time_to_vertex

    def run(self):
        """Runs all the code necessary in order for this object to work properly"""

        super().run()
        self.projectile_path.run(False, True, True)

    def run_collision(self, top_edge):
        """Runs all the code for figuring out what should happen when the ball collides with something by going down"""

        self.projectile_path.set_initial_distance(top_edge - self.height)
        self.projectile_path.reset()

        # So it lets the game know where the ball was previously; makes sure a collision doesn't happen next cycle
        # Because the ball was inside the platform when it wasn't
        self.top_edge = top_edge - self.height


class BouncyProjectileThrower(StraightProjectileThrower):
    """A projectile thrower except the projectiles bounce"""

    weapon_name = BOUNCY_PROJECTILE_WEAPON_NAME

    def __init__(self, use_action, user, user_max_velocity):
        """Initializes the object"""

        super().__init__(use_action, user, user_max_velocity)
        self.update_weapon_values(BOUNCY_THROWER_DAMAGE, BOUNCY_THROWER_HIT_POINTS, BOUNCY_THROWER_COOL_DOWN_TIME)

    def run_inanimate_object_collision(self, inanimate_object, index_of_sub_component):
        """Runs all the code for figuring ot what to do when one of the projectiles hits an inanimate object (platforms, trees, etc.)"""

        # No idea why this sometimes happens but sometimes there is a collision for a projectile that doesn't exist
        # So this must return if that happens otherwise the game crashes
        if index_of_sub_component >= len(self.collidable_components):
            return

        projectile: BouncyProjectile = self.collidable_components[index_of_sub_component]

        # Only the collision with the top of a platform should be handled differently
        if CollisionsEngine.is_top_collision(projectile, inanimate_object, True):
            projectile.run_collision(inanimate_object.top_edge)

        else:
            super().run_inanimate_object_collision(inanimate_object, index_of_sub_component)

    def run_upon_activation(self):
        """Runs the code that should be completed when the code decides to use this weapon"""

        if self.ammo_left > 0 or not self.has_limited_ammo:
            self.collidable_components.append(BouncyProjectile(self.get_weapon_left_edge(BOUNCY_PROJECTILE_SIZE, self.user.should_shoot_right),
                                                        self.user.projectile_top_edge, self.user.should_shoot_right,
                                                        self.user.projectile_height, self.user_max_velocity, self.object_type,
                                                        self.total_hit_points, self.user, f"games/platformer/images/{self.user_type}_bouncy_projectile"))
            self.ammo_left -= 1




