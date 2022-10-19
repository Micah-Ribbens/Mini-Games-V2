import abc

from games.platformer.weapons.weapon_user import WeaponUser
from game_dependencies.platformer.health_bar import HealthBar


class Enemy(WeaponUser, abc.ABC):
    """Anything that harms/attacks the player"""

    damage = 0
    is_moving_right = True
    platform = None
    damage = 10
    health_bar = None
    object_type = "Enemy"

    def __init__(self, damage, hit_points, platform, path_to_image):
        """Initializes the object"""

        self.damage, self.platform = damage, platform
        self.total_hit_points, self.hit_points_left = hit_points, hit_points
        super().__init__(path_to_image)
        self.health_bar = HealthBar(self)
        self.sub_components = [self]
        self.components = [self, self.health_bar]

    @abc.abstractmethod
    def run(self):
        pass

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

    def run_player_interactions(self, players):
        """ Runs all the code that should happen when the enemy and player interact: if the player sees the player it charges,
            The enemy tries to move towards the player, etc."""

        pass



