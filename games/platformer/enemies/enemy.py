import abc

from base.engines import CollisionsEngine
from base.history_keeper import HistoryKeeper
from games.platformer.weapons.weapon_user import WeaponUser
from game_dependencies.platformer.health_bar import HealthBar
from pygame_library.utility_functions import load_and_transform_image


class Enemy(WeaponUser, abc.ABC):
    """Anything that harms/attacks the player"""

    damage = 0
    is_moving_right = True
    platform = None
    damage = 10
    health_bar = None
    object_type = "Enemy"
    is_on_platform = True

    def __init__(self, damage, hit_points, platform, base_path_to_image):
        """Initializes the object"""

        super().__init__(base_path_to_image)

        self.damage, self.platform = damage, platform
        self.total_hit_points, self.hit_points_left = hit_points, hit_points
        self.health_bar = HealthBar(self)
        self.sub_components = [self]
        self.components = [self, self.health_bar]

    def run(self):
        pass

    def update_is_on_platform(self):
        # NOTE: From here on down *_collision_data[0] is if a user and a inanimate_object have collided
        # and *_collision_data[1] is the inanimate_object the user collided with
        self.is_on_platform = self.top_collision_data[0]

        if self.is_on_platform:
            self.platform = self.top_collision_data[1]

    def get_sub_components(self):
        """returns: Component[]; all the components that are collidable"""

        return self.sub_components

    def get_components(self):
        """returns: Component[]; all the components that should be ran and rendered"""

        return self.components

    def run_inanimate_object_collision(self, inanimate_object, index_of_sub_component, time):
        """Runs what should happen if the enemy or something the player threw hit an inanimate object"""

        if index_of_sub_component != self.index_of_user:
            self.weapon.run_inanimate_object_collision(inanimate_object, index_of_sub_component - self.weapon_index_offset, time)

        else:
            self.update_top_collision_data(inanimate_object, time)

    def update_top_collision_data(self, inanimate_object, time):
        """Updates the top_collision_data for the enemy"""

        is_same_coordinates = self.right_edge == inanimate_object.left_edge or self.left_edge == inanimate_object.right_edge
        is_top_collision = CollisionsEngine.is_top_collision(self, inanimate_object, True, time) and not is_same_coordinates

        # NOTE: From here on down *_collision_data[0] is if a user and a inanimate_object have collided
        # and *_collision_data[1] is the inanimate_object the user collided with
        if not self.top_collision_data[0] and is_top_collision:
            self.top_collision_data = [is_top_collision, inanimate_object]

    def run_player_interactions(self, players):
        """ Runs all the code that should happen when the enemy and player interact: if the player sees the player it charges,
            The enemy tries to move towards the player, etc."""

        pass



