from base.dimensions import Dimensions
import abc


# TODO come back to figuring out what weapons should do
from base.events import Event, TimedEvent
from base.utility_functions import key_is_pressed
from game_dependencies.platformer.platformer_constants import *


class Weapon(abc.ABC):
    """Something the user can use to hit enemies or anything else"""

    base_damage = WEAPON_BASE_DAMAGE
    damage = base_damage
    total_hit_points = 0
    hit_points_left = total_hit_points
    use_action = None
    use_key_event = None
    user = None
    collidable_components = []
    wait_event = None
    object_type = "" # Used for collisions, so the collision code knows the type of an object
    index = 0
    ammo_left = BASE_WEAPON_AMMO
    has_limited_ammo = True

    def __init__(self, damage, hit_points, use_action, user, cool_down_time):
        """Initilizes the object"""

        self.use_key_event = Event()
        self.use_action = use_action
        self.user = user
        self.name = id(self)
        self.wait_event = TimedEvent(cool_down_time, False)
        self.collidable_components = []
        self.object_type = f"{self.user.user_type} Weapon"

        self.update_weapon_values(damage, hit_points, cool_down_time)

    def run(self):
        self.use_key_event.run(self.use_action())
        self.wait_event.run(self.wait_event.current_time >= self.wait_event.time_needed, False)

        if self.use_key_event.is_click() and self.wait_event.has_finished():
            self.run_upon_activation()
            self.wait_event.start()

    def update_weapon_values(self, damage, hit_points, cool_down_time):
        """Updates the values of the weapon that can be modified"""

        self.base_damage, self.damage = damage, damage
        self.total_hit_points, self.hit_points_left = hit_points, hit_points
        self.wait_event.time_needed = cool_down_time

    def get_collidable_components(self):
        """returns: Component[]; all the sub components that must be rendered and have collisions for"""

        return self.collidable_components

    def get_weapon_left_edge(self, horizontal_length, is_facing_right):
        """returns: left_edge; the recommended x coordinate that the weapon should be at (right on the user)"""

        return self.user.right_edge if is_facing_right else self.user.left_edge - horizontal_length

    def reset(self):
        pass

    def update_for_side_scrolling(self, amount):
        pass

    @abc.abstractmethod
    def run_enemy_collision(self, enemy, index_of_sub_component):
        """Runs what should happen when an enemy and the weapon collide"""
        pass

    @abc.abstractmethod
    def run_inanimate_object_collision(self, inanimate_object, index_of_sub_component):
        """Runs what should happen when the weapon and an inanimate object collide"""
        pass

    @abc.abstractmethod
    def run_upon_activation(self):
        """Runs what should happen when the person who plays the game tries to use the weapon"""
        pass

    @abc.abstractmethod
    def reset(self):
        """Resets everything back to the start of the game"""
        pass

