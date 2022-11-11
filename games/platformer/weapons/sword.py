import math

from base.lines import Point, LineSegment
from base.events import TimedEvent
from base.important_variables import screen_length
from base.velocity_calculator import VelocityCalculator
from games.platformer.weapons.weapon import Weapon

# TODO figure out the sword
# TODO do collision logic for the sword
class Sword(Weapon):
    """Something the user can use to hit enemies with"""

    full_extension_time = 2
    extending_timed_event = None
    start_point = None
    end_point = None
    length = VelocityCalculator.get_measurement(screen_length, 10)
    is_moving_right = False
    index = 0

    def __init__(self, use_action, user):
        """Initializes the object"""

        # Have to add the 'full_extension_time' because the cooldown time starts when the user does the use_action
        super().__init__(20, 0, use_action, user, self.full_extension_time + .2)
        self.extending_timed_event = TimedEvent(self.full_extension_time, False)
        self.index = self.user.weapon_index_offset

    def run(self):
        """Runs all the code necessary in order for this weapon to work"""

        super().run()
        self.extending_timed_event.run(self.extending_timed_event.current_time > self.extending_timed_event.time_needed, False)

        if not self.extending_timed_event.has_finished():
            self.start_point = Point(self.get_weapon_left_edge(0, self.is_moving_right), self.user.projectile_top_edge)
            self.end_point = Point(self.start_point.left_edge + self.get_horizontal_displacement(),
                                   self.start_point.y_coordinate - self.get_vertical_displacement())

        # If the sword is not extending then it's length should be 0 so it doesn't render or cause collisions
        else:
            self.start_point, self.end_point = Point(0, 0), Point(0, 0)

    def run_enemy_collision(self, user, index_of_sub_component):
        """Runs what should happen when the user and the weapon collide"""

        user.cause_damage(self.damage)

    def reset(self):
        """Resets everything back to the start of the game"""

        self.extending_timed_event.reset()

    def run_inanimate_object_collision(self, inanimate_object, index_of_sub_component):
        """Runs what should happen when the weapon and an inanimate object collide"""

        pass

    def run_upon_activation(self):
        """Runs what should happen when the person who plays the game tries to use the weapon"""

        self.extending_timed_event.start()
        self.is_moving_right = self.user.should_shoot_right

    def get_horizontal_displacement(self):
        """returns: double; the horizontal displacement from the user (based on the user's direction)"""

        distance = math.sin(self.get_radians()) * self.length
        return distance if self.is_moving_right else -distance

    def get_vertical_displacement(self):
        """returns: double; the vertical displacement from the user"""

        return math.cos(self.get_radians()) * self.length

    def get_radians(self):
        """returns: double; the radian amount of the sword"""

        fraction_of_full_time = self.extending_timed_event.current_time / self.full_extension_time
        return math.pi * fraction_of_full_time




