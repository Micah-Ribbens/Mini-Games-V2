from base.engines import CollisionsEngine
from base.quadratic_equations import PhysicsPath
from games.platformer.weapons.projectile_thrower import Projectile, ProjectileThrower


class BouncyProjectile(Projectile):
    """A projectile that bounces"""

    projectile_path = None

    def __init__(self, left_edge, top_edge, is_moving_right, projectile_height, user_velocity, object_type, total_hit_points, user, path_to_image):
        """Initializes the object"""

        super().__init__(left_edge, top_edge, is_moving_right, user_velocity, object_type, total_hit_points, user, path_to_image)
        time_to_vertex = .2
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


class BouncyProjectileThrower(ProjectileThrower):
    """A projectile thrower except the projectiles bounce"""

    def run_inanimate_object_collision(self, inanimate_object, index_of_sub_component, time):
        """Runs all the code for figuring ot what to do when one of the projectiles hits an inanimate object (platforms, trees, etc.)"""

        # No idea why this sometimes happens but sometimes there is a collision for a projectile that doesn't exist
        # So this must return if that happens otherwise the game crashes
        if index_of_sub_component >= len(self.sub_components):
            return

        projectile: BouncyProjectile = self.sub_components[index_of_sub_component]

        # Only the collision with the top of a platform should be handled differently
        if CollisionsEngine.is_top_collision(projectile, inanimate_object, True, time):
            projectile.run_collision(inanimate_object.top_edge)

        else:
            super().run_inanimate_object_collision(inanimate_object, index_of_sub_component, time)

    def run_upon_activation(self):
        """Runs the code that should be completed when the code decides to use this weapon"""

        self.sub_components.append(BouncyProjectile(self.get_weapon_left_edge(Projectile.size, self.user.should_shoot_right),
                                                    self.user.projectile_top_edge, self.user.should_shoot_right,
                                                    self.user.projectile_height, self.user.projectile_velocity, self.object_type,
                                                    self.total_hit_points, self.user, "games/platformer/images/player_bouncy_projectile.png"))


