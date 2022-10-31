import abc

from gui_components.component import Component
from base.engines import CollisionsEngine
from base.important_variables import screen_length
from base.velocity_calculator import VelocityCalculator
from pygame_library.utility_functions import load_and_transform_image, get_direction_path_to_image


class WeaponUser(Component):
    """A class that provides what is needed for a weapon to function"""

    max_velocity = 0
    is_facing_right = False
    hit_points_left = 0
    total_hit_points = 0
    weapon = None
    weapon_index_offset = 1
    index_of_user = 0
    index = 0
    is_on_platform = True
    sub_components = []
    is_addable = True
    base_path_to_image = ""

    # Collision Data
    left_collision_data = [False, None]
    right_collision_data = [False, None]
    top_collision_data = [False, None]
    bottom_collision_data = [False, None]
    components = []

    def __init__(self, base_path_to_image):
        """Initializes the object"""

        load_and_transform_image(base_path_to_image)
        super().__init__(f"{base_path_to_image}_left.png")
        self.base_path_to_image = base_path_to_image

        self.sub_components = [self]
        self.components = []

    @property
    def projectile_velocity(self):
        return self.max_velocity

    @property
    def projectile_top_edge(self):
        return self.vertical_midpoint

    @property
    def projectile_height(self):
        return self.height / 2

    @property
    def should_shoot_right(self):
        return self.is_facing_right

    @property
    def user_type(self):
        return self.object_type

    def run_inanimate_object_collision(self, inanimate_object, index_of_sub_component, time):
        """Runs what should happen when the weapon and an inanimate object collide"""

        self.weapon.run_inanimate_object_collision(inanimate_object, index_of_sub_component - 1, time)

    def run_enemy_collision(self, enemy, index_of_sub_component):
        """Runs what should happen when the weapon user hits an 'enemy' (the user would be the enemy's 'enemy')"""

        if index_of_sub_component == self.index_of_user:
            enemy.cause_damage(self.damage)

        elif self.weapon is not None:
            self.weapon.run_enemy_collision(enemy, index_of_sub_component - self.weapon_index_offset)

    def run_upon_activation(self):
        """Runs what should happen when the person who plays the game tries to use the weapon"""

        self.weapon.run_upon_activation()

    def get_sub_components(self):
        """returns: Component[]; all the components that should be ran and rendered"""

        return self.sub_components

    def reset_collision_data(self):
        """Resets all the collision data from the previous cycle, so it can do collisions for this cycle"""

        self.left_collision_data, self.right_collision_data, self.top_collision_data, self.bottom_collision_data = [False, None], [False, None], [False, None], [False, None]

    def get_collision_data(self, inanimate_object, is_collision, time):
        """returns: Boolean[4]; [is_left_collision, is_right_collision, is_top_collision, is_bottom_collision] --> the
           collision data gotten from the inanimate_object and is by the perspective of the user (has the user collided with the inanimate_object's right_edge)"""

        is_same_coordinates = self.right_edge == inanimate_object.left_edge or self.left_edge == inanimate_object.right_edge

        return [CollisionsEngine.is_left_collision(self, inanimate_object, is_collision, time),
                CollisionsEngine.is_right_collision(self, inanimate_object, is_collision, time),
                CollisionsEngine.is_top_collision(self, inanimate_object, is_collision, time) and not is_same_coordinates,
                CollisionsEngine.is_bottom_collision(self, inanimate_object, is_collision, time) and not is_same_coordinates]

    def update_collision_data(self, inanimate_object, current_collision_data, is_collision):
        """Updates the values of the 'current_collision_data' to reflect 'is_collision' and 'inanimate_object'"""
        
        # NOTE: From here own down *_collision_data[0] is if a user and a inanimate_object have collided
        # and *_collision_data[1] is the inanimate_object the user collided with
        if not current_collision_data[0] and is_collision:
            current_collision_data[0], current_collision_data[1] = is_collision, inanimate_object

    def update_platform_collision_data(self, inanimate_object, time):
        """Updates all the inanimate_object collision data"""

        is_left_collision, is_right_collision, is_top_collision, is_bottom_collision = self.get_collision_data(inanimate_object, True, time)

        self.update_collision_data(inanimate_object, self.left_collision_data, is_left_collision)
        self.update_collision_data(inanimate_object, self.right_collision_data, is_right_collision)
        self.update_collision_data(inanimate_object, self.top_collision_data, is_top_collision)
        self.update_collision_data(inanimate_object, self.bottom_collision_data, is_bottom_collision)

    def run_collisions(self, time):
        """Runs what should happen based on what got stored in the collision data (nothing is a possibility like possibly an enemy)"""

        pass

    def cause_damage(self, amount):
        """Damages the weapon user by that amount"""

        self.hit_points_left -= amount

    def update_for_side_scrolling(self, amount):
        self.left_edge -= amount

        # Some Enemies don't have weapons, so an error will be thrown if we try to call the weapon's update_for_side_scrolling()
        if self.weapon is not None:
            self.weapon.update_for_side_scrolling(amount)

    def render(self):
        """Renders the object onto the screen"""

        self.path_to_image = get_direction_path_to_image(self.base_path_to_image, self.is_facing_right, "")
        super().render()

    def get_components(self):
        """returns: Component[]; all the components that should be rendered and ran"""

        return self.sub_components

