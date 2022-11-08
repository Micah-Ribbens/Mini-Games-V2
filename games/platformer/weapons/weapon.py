from base.dimensions import Dimensions
import abc


# TODO come back to figuring out what weapons should do
from base.events import Event, TimedEvent
from base.utility_functions import key_is_pressed
from game_dependencies.platformer.platformer_variables import *


class Weapon(abc.ABC):
    """Something the user can use to hit enemies or anything else"""

    base_damage = 10
    damage = base_damage
    total_hit_points = 10
    hit_points_left = 0
    use_action = None
    use_key_event = None
    user = None
    sub_components = []
    wait_event = None
    object_type = "" # Used for collisions, so the collision code knows the type of an object
    index = 0
    ammo_left = base_weapon_ammo
    has_limited_ammo = True

    def __init__(self, damage, hit_points, use_action, user, cool_down_time):
        """Initilizes the object"""

        self.use_key_event = Event()
        self.damage, self.use_action = damage, use_action
        self.total_hit_points, self.hit_points_left = hit_points, hit_points
        self.user = user
        self.name = id(self)
        self.wait_event = TimedEvent(cool_down_time, False)
        self.sub_components = [self]
        self.object_type = f"{self.user.user_type} Weapon"

    def run(self):
        self.use_key_event.run(self.use_action())
        self.wait_event.run(self.wait_event.current_time >= self.wait_event.time_needed, False)

        if self.use_key_event.is_click() and self.wait_event.has_finished():
            self.run_upon_activation()
            self.wait_event.start()

    def get_sub_components(self):
        """returns: GameObject[0]; all the sub components that must be rendered and have collisions for"""

        return self.sub_components

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
    def run_inanimate_object_collision(self, inanimate_object, index_of_sub_component, time):
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

