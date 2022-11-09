from math import sqrt

from base.colors import red, light_gray, white
from base.engines import CollisionsEngine
from base.lines import LineSegment, Point
from base.events import Event, TimedEvent
from base.game_movement import GameMovement

from base.quadratic_equations import PhysicsPath
from base.history_keeper import HistoryKeeper
from base.utility_functions import key_is_pressed, solve_quadratic, key_is_hit, key_has_been_released
from base.velocity_calculator import VelocityCalculator
from games.platformer.weapons.bouncy_projectile_thrower import BouncyProjectileThrower
from games.platformer.weapons.straight_projectile_thrower import StraightProjectileThrower
from games.platformer.weapons.sword import Sword
from game_dependencies.platformer.platformer_variables import *
from games.platformer.weapons.weapon_user import WeaponUser
from base.important_variables import *


class Player(WeaponUser):
    # Modifiable numbers
    max_jump_height = PLAYER_JUMP_DISPLACEMENT
    running_deceleration_time = PLAYER_RUNNING_DECELERATION_TIME
    base_top_edge = PLAYER_BASE_TOP_EDGE
    base_left_edge = PLAYER_BASE_LEFT_EDGE
    max_velocity = PLAYER_MAX_HORIZONTAL_VELOCITY
    time_to_get_to_max_velocity = PLAYER_TIME_TO_GET_MAX_VELOCITY
    total_hit_points = PLAYER_TOTAL_HIT_POINTS
    hit_points_left = total_hit_points
    object_type = PLAYER_OBJECT_TYPE
    length = PLAYER_LENGTH
    height = PLAYER_HEIGHT
    ammo_left = BASE_WEAPON_AMMO
    weapon_class_to_weapon = {}

    # Miscellaneous
    jumping_path = None
    deceleration_path = None
    acceleration_path = None
    current_velocity = 0
    initial_upwards_velocity = 0
    paths_and_events = None
    gravity_engine = None
    invincibility_event = None
    platform_is_on = None
    last_platform_was_on = None

    # So the player can be run and side scrolling can be done before the rendering (otherwise it doesn't look smooth)
    is_runnable = False

    # Booleans
    can_move_down = False
    can_move_left = False
    can_move_right = False
    is_on_platform = True
    is_facing_right = True

    # Keys
    left_key = None
    right_key = None
    jump_key = None
    down_key = None
    attack_key = None

    def __init__(self, left_key, right_key, jump_key, down_key, attack_key):
        """Initializes the object"""

        super().__init__("games/platformer/images/player")

        self.left_key, self.right_key, self.jump_key = left_key, right_key, jump_key
        self.down_key, self.attack_key = down_key, attack_key

        self.jumping_path = PhysicsPath(game_object=self, attribute_modifying="top_edge", height_of_path=-PLAYER_JUMP_DISPLACEMENT, initial_distance=self.top_edge, time=PLAYER_TIME_TO_JUMP_VERTEX)
        self.jumping_path.set_initial_distance(self.top_edge)
        self.acceleration_path = PhysicsPath()
        self.acceleration_path.set_acceleration_with_velocity(self.time_to_get_to_max_velocity, self.max_velocity)
        self.deceleration_path = PhysicsPath(game_object=self, attribute_modifying="left_edge", max_time=self.running_deceleration_time)
        self.initial_upwards_velocity = self.jumping_path.initial_velocity

        self.jumping_event, self.right_event, self.left_event = Event(), Event(), Event()

        self.invincibility_event = TimedEvent(PLAYER_INVINCIBILITY_TOTAL_TIME, False)
        self.paths_and_events = [self.jumping_path, self.deceleration_path, self.acceleration_path]

        weapon_data = [lambda: key_is_pressed(self.attack_key), self]
        self.weapon_class_to_weapon = {StraightProjectileThrower.weapon_name: StraightProjectileThrower(*weapon_data),
                                       BouncyProjectileThrower.weapon_name: BouncyProjectileThrower(*weapon_data)}
        self.weapon = self.weapon_class_to_weapon[BouncyProjectileThrower.weapon_name]

    def run(self):
        """Runs all the code that is necessary for the player to work properly"""

        self.is_facing_right = True if key_is_pressed(self.right_key) else self.is_facing_right
        self.is_facing_right = False if key_is_pressed(self.left_key) else self.is_facing_right

        self.weapon.run()
        self.ammo_left = self.weapon.ammo_left
        self.jumping_path.run(False, False)
        self.sub_components = [self] + self.weapon.get_sub_components()
        self.invincibility_event.run(self.invincibility_event.current_time > self.invincibility_event.time_needed, False)

        if self.jumping_path.has_finished() and key_is_hit(self.jump_key):
            self.jump()

        if self.top_edge <= 0:
            self.run_bottom_edge_collision(0)

        if key_has_been_released(self.right_key) or key_has_been_released(self.left_key):
            self.decelerate_player(key_has_been_released(self.right_key))
            self.acceleration_path.reset()

        GameMovement.player_horizontal_movement(self, self.current_velocity, self.left_key, self.right_key)
        if self.deceleration_path.has_finished() or self.player_movement_direction_is_same_as_deceleration():
            # TODO figure out what this does
            self.update_acceleration_path()
            self.deceleration_path.reset()

        elif self.can_decelerate():
            self.deceleration_path.run(False, False, is_changing_coordinates=False)

            self.left_edge += self.deceleration_path.get_total_displacement()

        # If the player is facing a direction, but the player can't move that direction that means the player can't decelerate or accelerate
        should_reset_paths = (self.is_facing_right and not self.can_move_right) or (not self.is_facing_right and not self.can_move_left)
        if should_reset_paths:
            self.deceleration_path.reset()
            self.acceleration_path.reset()

    def set_is_on_platform(self, is_on_platform, platform_is_on):
        """Sets the player's is on platform attribute"""

        if not self.is_on_platform and is_on_platform:
            self.jumping_path.reset()
            self.jumping_path.set_initial_distance(self.top_edge)
            self.jumping_path.initial_velocity = self.initial_upwards_velocity

        self.last_platform_was_on = platform_is_on if is_on_platform else self.last_platform_was_on
        self.platform_is_on = platform_is_on if is_on_platform else None
        self.is_on_platform = is_on_platform

    def reset(self):
        """Resets the player back to the start of the game"""

        self.left_edge = self.base_left_edge
        self.top_edge = self.base_top_edge

        self.weapon.reset()
        self.run_respawning()  # Resetting from the game ending and respawning has a lot in similarity

    def run_respawning(self):
        """Makes the player respawn (resets most things)"""

        self.is_on_platform = True
        self.jumping_path.initial_velocity = self.initial_upwards_velocity
        self.hit_points_left = self.total_hit_points
        self.invincibility_event.reset()

        # Resetting the direction the player can move
        self.can_move_left, self.can_move_right, self.can_move_down = False, False, False

        for path_or_event in self.paths_and_events:
            path_or_event.reset()

    def set_top_edge(self, top_edge):
        """Sets the y coordinate of the player"""

        self.jumping_path.set_initial_distance(top_edge)
        self.top_edge = top_edge

    def jump(self):
        """Makes the player jump"""

        self.jumping_path.start()
        self.gravity_engine.game_object_to_physics_path[self].reset()

    def decelerate_player(self, is_moving_right):
        """Makes the player decelerate by calling deceleration_path.start()"""

        self.deceleration_path.initial_distance = self.left_edge
        self.deceleration_path.initial_velocity = self.current_velocity if is_moving_right else -self.current_velocity

        # If the player is not at maximum velocity it shouldn't take as long to decelerate
        fraction_of_max_velocity = self.current_velocity / self.max_velocity
        time_needed = self.running_deceleration_time * fraction_of_max_velocity

        # Gotten using math; Makes the player stop in the amount of time 'self.running_deceleration_time'
        self.deceleration_path.acceleration = (-self.deceleration_path.initial_velocity) / time_needed

        self.deceleration_path.start()
        self.deceleration_path.max_time = time_needed

    def player_movement_direction_is_same_as_deceleration(self):
        """returns: boolean; if the direction the player is moving is equal to the deceleration"""

        deceleration_direction_is_rightwards = self.deceleration_path.acceleration < 0
        return ((deceleration_direction_is_rightwards and key_is_pressed(self.right_key)) or
                not deceleration_direction_is_rightwards and key_is_pressed(self.left_key))

    def update_acceleration_path(self):
        """Updates the time of the acceleration_path, so that if the deceleration has not finished then it will pick up
            at the velocity where the deceleration ended at"""

        deceleration_has_not_finished = self.deceleration_path.current_time > 0
        
        if deceleration_has_not_finished:
            current_velocity = self.deceleration_path.get_velocity_using_time(self.deceleration_path.current_time)
            self.acceleration_path.start()
            # Figuring out the time to get to that velocity, so the player can continue to accelerate to the max velocity
            self.acceleration_path.current_time = sqrt(abs(current_velocity) / self.acceleration_path.acceleration)

        GameMovement.run_acceleration(self, key_is_pressed(self.left_key) or key_is_pressed(self.right_key), self.acceleration_path)

    def can_decelerate(self):
        """returns: boolean; if the player can decelerate (they couldn't if an object was in the way"""

        deceleration_direction_is_rightwards = self.deceleration_path.acceleration < 0
        return self.can_move_right if deceleration_direction_is_rightwards else self.can_move_left

    def run_bottom_edge_collision(self, top_edge):
        """Runs what should happen after a bottom collision (the player should rebound off of it)"""

        velocity = self.jumping_path.get_velocity_using_displacement(self.jumping_path.initial_distance + top_edge)
        self.jumping_path.set_variables(initial_velocity=velocity)
        self.jumping_path.reset()
        self.top_edge = top_edge

    def get_velocity(self):
        """returns: double; the current velocity of the player"""

        return_value = None
        if self.deceleration_path.has_finished():
            return_value = self.current_velocity

        else:
            return_value = self.deceleration_path.get_velocity_using_time(self.deceleration_path.current_time)

        return return_value

    # Collision Stuff
    def run_inanimate_object_collision(self, inanimate_object, index_of_sub_component, time):
        """Runs what should happen when the player collides with an inanimate object"""

        if index_of_sub_component == self.index_of_user:
            self.update_platform_collision_data(inanimate_object, time)

        if index_of_sub_component != self.index_of_user:
            self.weapon.run_inanimate_object_collision(inanimate_object, index_of_sub_component - self.weapon_index_offset, time)

    def run_collisions(self, time):
        """Runs what should happen based on what got stored in the collision data"""

        # The player should only act upon the collision data if there was stuff in the History Keeper because if there wasn't
        # Then the game is automatically going to say it was not a collision (top, left, right, bottom)
        # TODO change to HistoryKeeper.get_last_using_time?
        if HistoryKeeper.get_last(self.name) is not None:
            self.alter_player_horizontal_movement()
            self.alter_player_vertical_movement()

    def alter_player_horizontal_movement(self):
        """Alters the player's horizontal movement so it stays within the screen and is not touching the platforms"""

        player_is_beyond_screen_left = self.left_edge <= 0
        player_is_beyond_screen_right = self.right_edge >= screen_length

        # The deceleration must be going left to stop the player from moving right and vice versa
        deceleration_is_rightwards = self.deceleration_path.acceleration < 0

        is_decelerating_rightwards = not self.deceleration_path.has_finished() and deceleration_is_rightwards
        is_decelerating_leftwards = not self.deceleration_path.has_finished() and not deceleration_is_rightwards

        self.can_move_left = not self.right_collision_data[0] and not player_is_beyond_screen_left and not is_decelerating_rightwards
        self.can_move_right = not self.left_collision_data[0] and not player_is_beyond_screen_right and not is_decelerating_leftwards

        # Setting the player's x coordinate if the any of the above conditions were met (collided with platform or beyond screen)
        self.change_attribute_if(player_is_beyond_screen_left, self.set_left_edge, 0)
        self.change_attribute_if(player_is_beyond_screen_right, self.set_left_edge, screen_length - self.length)

        if self.right_collision_data[0]:
            self.set_left_edge(self.right_collision_data[1].right_edge)

        if self.left_collision_data[0]:
            self.set_left_edge(self.left_collision_data[1].left_edge - self.length)

    def alter_player_vertical_movement(self):
        """Alters the player's vertical movement so it can't go through platforms"""

        player_is_on_platform = self.top_collision_data[0]

        if player_is_on_platform:
            self.set_top_edge(self.top_collision_data[1].top_edge - self.height)
            self.gravity_engine.game_object_to_physics_path[self].reset()

        self.set_is_on_platform(player_is_on_platform, self.top_collision_data[1])

        if self.bottom_collision_data[0]:
            self.gravity_engine.game_object_to_physics_path[self].reset()
            self.run_bottom_edge_collision(self.bottom_collision_data[1].bottom_edge)
    @property
    def is_beyond_screen_left(self):
        self.left_edge <= 0

    @property
    def is_beyond_screen_right(self):
        self.right_edge >= screen_length

    def set_left_edge(self, left_edge):
        self.left_edge = left_edge

    def change_attribute_if(self, condition, function, value):
        """Changes the attribute to the value if 'condition()' is True"""

        if condition:
            function(value)

    def cause_damage(self, amount):
        """Damages the player by that amount and also starts the player's invincibility"""

        if self.invincibility_event.has_finished():
            self.hit_points_left -= amount
            self.invincibility_event.start()

    def get_topmost_top_edge(self, last_platform, accuracy, min_accuracy):
        """ summary: Figures out the minimum y coordinate of the next platform (remember the closer to the top of the screen the lower the y coordinate)

            params:
                last_platform: Platform; the platform the player would be jumping from
                margin_of_error: double; how accurate the player has to be to clear this jump
                min_accuracy: double; the minimum accuracy possible

            returns: double; max y coordinate that the next platform could be at that leaves the player 'margin_of_error'
        """

        max_jump_height = self.max_jump_height
        topmost_top_edge = last_platform.top_edge - (max_jump_height * accuracy) + self.height

        # The absolute max of a platform is the player's height because the player has to get its bottom_edge on the platform
        # Which would mean the player's y coordinate would be 0 also
        max_buffer = VelocityCalculator.get_measurement(screen_height, 25)
        buffer = LineSegment(Point(1, 0), Point(min_accuracy, max_buffer)).get_y_coordinate(accuracy)
        if topmost_top_edge <= self.height + buffer:
            topmost_top_edge = self.height + buffer

        return topmost_top_edge

    def get_distance_to_reach_max_velocity(self):
        """returns: double; the distance needed for the player to reach max velocity"""

        time_needed = self.max_velocity / self.acceleration_path.acceleration
        return self.acceleration_path.get_distance(time_needed)

    def get_max_time_to_top_edge(self, start_top_edge, new_top_edge):
        """returns; double; the max amount of time for the player's bottom_edge to reach the new y coordinate"""

        # TODO change this value if gravity is not the same as the player's jumping path
        gravity = self.jumping_path.acceleration

        vertex_top_edge = start_top_edge - self.max_jump_height
        total_distance = self.max_jump_height + (new_top_edge - vertex_top_edge)

        # Since the y distance the player travels is constant and the distance from where the player jumped and the
        # vertex of the jump stays constant, then in order to optimize the jump the player has to be at the same velocity
        # on both sides of the jump -> vertex parabola (max_jump_height). This would then mean that the player would have to travel the
        # same distance on both sides because "vf = vi + at" and vi is 0 for both. This then would mean that:
        # "1/2 * at^2 = 1/2 * (total_distance - max_jump_height)"
        one_side_falling_time = solve_quadratic(1/2 * gravity, 0, -1/2 * (total_distance - self.max_jump_height))[1]

        falling_distance = self.jumping_path.get_acceleration_displacement_from_time(one_side_falling_time)
        player_vertex_after_jump = falling_distance + start_top_edge - self.max_jump_height

        # The player can't jump beyond the top of the screen, so that has to be checked (also since the other 'top_edges'
        # Are actually the bottom_edge of the player then I have to substract that to figure out the 'actual_top_edge'
        if player_vertex_after_jump - self.height <= 0:
            falling_distance = self.max_jump_height - start_top_edge + self.height

        # First and second falling times are in relation to what side of the jump -> vertex parabola
        first_falling_time = solve_quadratic(1/2 * gravity, 0, -falling_distance)[1]
        vertex_top_edge = start_top_edge + falling_distance - self.max_jump_height
        second_falling_distance = new_top_edge - vertex_top_edge

        second_falling_times = solve_quadratic(1/2 * gravity, 0, -second_falling_distance)
        second_falling_time = second_falling_times[0]

        # The other side of the parabola is needed if the length is 2 (the other side is a negative number)
        if len(second_falling_times) == 2:
            second_falling_time = second_falling_times[1]

        return first_falling_time + second_falling_time + PLAYER_TIME_TO_JUMP_VERTEX

    def get_total_time(self, start_top_edge, gravity, new_top_edge, falling_distance):
         # First and second falling times are in relation to what side of the jump -> vertex parabola
        first_falling_time = solve_quadratic(1 / 2 * gravity, 0, -falling_distance)[1]
        vertex_top_edge = start_top_edge + falling_distance - self.max_jump_height
        second_falling_distance = new_top_edge - vertex_top_edge
        second_falling_time = solve_quadratic(1 / 2 * gravity, 0, -second_falling_distance)[1]

        return f"total time {first_falling_time + second_falling_time + PLAYER_TIME_TO_JUMP_VERTEX} first falling time {first_falling_time} second falling time {second_falling_time}"

    # Getters and Setters
    def increase_ammo(self, amount):
        """Increases the amount of ammo of the weapon"""

        self.ammo_left += amount
        self.weapon.ammo_left += amount

    def increase_health(self, amount):
        """Increases the amount of health the player has"""

        self.hit_points_left += amount

        # The player's current hit points can't increase the total hit points
        if self.hit_points_left > self.total_hit_points:
            self.hit_points_left = self.total_hit_points

    def set_weapon(self, weapon_class):
        """Changes the player's weapon to that weapon (ammo is kept the same)"""

        if self.weapon.weapon_name == weapon_class.weapon_name:
            self.weapon.damage += DAMAGE_INCREASE_FROM_DUPLICATE_WEAPON_PICKUP

        else:
            self.weapon = self.weapon_class_to_weapon[weapon_class.weapon_name]
            self.weapon.damage = self.weapon.base_damage
            self.weapon.ammo_left = self.ammo_left

    def get_ammo_left(self):
        """returns: int; the amount of ammo the player has left"""

        return self.ammo_left




