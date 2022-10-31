from base.important_variables import screen_height
from base.utility_functions import get_kwarg_item, solve_quadratic
from base.velocity_calculator import VelocityCalculator


class QuadraticEquation:
    """A class that defines the necessary variables for a quadratic ax^2 + bx + c"""
    h = 0
    k = 0
    a = 0

    def set_variables(self, h, k, a):
        """ summary: sets the variables to the numbers to equation: a(x-h)^2 + k

            params:
                h: double; the first number of the vertex
                k: double; the second number of the vertex
                a: double; the number that goes before (x-h)^2

            returns: None
        """

        self.h = h
        self.k = k
        self.a = a

    def get_number(self, x):
        """ summary: finds the number by plugging x into the equation ax^2 + bx + c

            params:
                x: double; the variable x that will be used to get the number

            returns: double; the number that is gotten when x is plugged into the equation
        """

        return self.a * pow((x - self.h), 2) + self.k

    def points_set_variables(self, vertex, other_point):
        """ summary: sets the variables based on both points

            params:
                vertex: Point; the vertex of the quadratic equation
                other_point: Point; another point besides the vertex

            returns: None
        """

        self.h = vertex.x_coordinate
        self.k = vertex.y_coordinate

        # Figured this out using algebra
        self.a = (other_point.y_coordinate - self.k) / pow((other_point.x_coordinate - self.h), 2)


# TODO fix jumping logic again; go back to original design (that is a huge rip lol) ---> or do I...
class PhysicsEquation:
    """A class that uses common physics equations for initial_velocity, acceleration, and initial_distance"""

    acceleration = 0
    initial_velocity = 0
    initial_distance = 0

    def get_time_to_vertex(self):
        """ summary: gets the time it takes to reach the vertex knowing that the final initial_velocity is 0, so the time is -initial_velocity / acceleration
            params: None
            returns: double; the time to reach the vertex
        """

        return -self.initial_velocity / self.acceleration

    def set_acceleration_with_displacement(self, time, displacement):
        """ summary: sets the acceleration knowing that d = 1/2 * a * t^2 where d is displacement, a is acceleration, and t is time

            params:
                time_to_fall: double; the amount of time that it should take to go that amount (displacement)
                time: double; the distance (up being positive and down being negative) that it should travel

            returns: None
        """

        self.acceleration = (2 * displacement) / pow(time, 2)

    def set_acceleration_with_velocity(self, time, velocity_change):
        """Sets the acceleration knowing that vf = vi + at"""

        self.acceleration = velocity_change / time

    def set_all_variables(self, vertex, time, initial_distance):
        """ summary: sets all the variables; calls set_velocity and set_gravity_acceleration

            params:
                vertex: double; the highest/lowest point of the parabola
                time: double; the time it takes to get to the vertex/go the acceleration_distance
                acceleration_displacement: double; the distance (up being positive and down being negative) that the acceleration in that time
                initial_distance: double; the initial distance

            returns: None
        """

        self.initial_distance = initial_distance

        # Gotten using math
        self.initial_velocity = (-2 * initial_distance + 2 * vertex) / time
        self.acceleration = 2 * (initial_distance - vertex) / pow(time, 2)

    def set_variables(self, **kwargs):
        """ summary: sets the variables to the number provided

            params:
                acceleration: double; the acceleration (can be positive or negative) | a in 1/2 * ax^2 + bx + c
                initial_velocity: double; the initial_velocity (can be positive or negative) | b in 1/2 * ax^2 + bx + c
                initial_distance: double; the starting point (can be positive or negative) | c in 1/2 * ax^2 + bx + c

            returns: None
        """

        self.acceleration = get_kwarg_item(kwargs, "acceleration", self.acceleration)
        self.initial_velocity = get_kwarg_item(kwargs, "initial_velocity", self.initial_velocity)
        self.initial_distance = get_kwarg_item(kwargs, "initial_distance", self.initial_distance)

    def get_distance(self, time):
        """ summary: finds the number by plugging x into the equation 1/2 * at^2 + vt + d
                     where a is acceleration, t is time, v is initial_velocity, and d is initial_distance

            params:
                time: double; the amount of time that has passed

            returns: double; the number that is gotten when time is plugged into the equation
        """
        return 1 / 2 * self.acceleration * pow(time, 2) + self.initial_velocity * time + self.initial_distance

    def get_velocity_using_time(self, time):
        """ summary: uses the fact that the initial_velocity is equal to vi - at^2 where vi is the initial initial_velocity, a is acceleration, and t is time
                     to find the initial_velocity

            params:
                time: double; the amount of time that the initial_velocity has been affected by acceleration

            returns: double; the initial_velocity after affected by acceleration
        """

        return self.initial_velocity + self.acceleration * time

    def get_velocity_using_displacement(self, displacement):
        """ summary: uses the formula vf^2 = vi^2 + 2ax to find the initial_velocity
                     where vf is final initial_velocity, vi is initial initial_velocity, a is acceleration, and x is displacement

            params:
                displacement: double; the amount that the ball has traveled (upwards is positive and downwards is negative)

            returns: double; the final initial_velocity
        """

        final_velocity_squared = pow(self.initial_velocity, 2) + 2 * self.acceleration * displacement
        # Reduces the risk of a rounding error like -1*e^-15 would cause an imaginary number exception
        return pow(int(final_velocity_squared), 1 / 2)

    def get_vertex(self):
        """returns: double; the vertex of this physics equation"""

        return self.get_distance(self.get_time_to_vertex())

    def get_times_to_point(self, distance):
        """ summary: finds the number by plugging in 'distance' into the equation 1/2 * at^2 + vt + d
                     where a is acceleration, t is time, v is initial_velocity, and d is initial_distance

            params:
                distance: double; the distance that is wanted

            returns: List of double; the times that the parabola is at that y coordinate
        """
        return solve_quadratic(1 / 2 * self.acceleration, self.initial_velocity, self.initial_distance - distance)

    def get_full_cycle_time(self):
        """returns: double; the amount of time it takes the parabola to go from start_location -> start_location"""

        return self.get_time_to_vertex() * 2

    def __str__(self):
        return f"[{self.acceleration},{self.initial_velocity},{self.initial_distance},]"

    def __eq__(self, other):
        return (self.acceleration == other.acceleration and self.initial_velocity == other.initial_velocity and
                self.initial_distance == other.initial_distance)


class PhysicsPath(PhysicsEquation):
    """An extension of physics equation that allows for automatically changing the player's coordinates"""

    game_object = None
    current_time = 0
    is_started = False
    attribute_modifying = None
    height_of_path = 0
    time = 0
    max_time = 0
    last_time = 0
    has_max_time = False
    all_distance = 0
    last_delta_time = 0

    # def __init__(self, game_object=None, attribute_modifying="", height_of_path=0, initial_distance=0, time=.5):
    def __init__(self, **kwargs):
        """ summary: initializes the object

            params:
                game_object: GameObject; the game object that is following this path
                attribute_modifying: String; the name of the attribute this path is modifying
                time: double; the time to the vertex of the path
                height_of_path: double; the difference between the initial distance and the vertex of the path
                max_time: double; the max time of the path- the time the path should end

            returns: None
        """

        """Initializes the object"""

        self.game_object, self.attribute_modifying = get_kwarg_item(kwargs, "game_object", None), get_kwarg_item(kwargs,
                                                                                                                 "attribute_modifying",
                                                                                                                 "")
        self.time, self.height_of_path = get_kwarg_item(kwargs, "time", .5), get_kwarg_item(kwargs, "height_of_path", 0)
        self.initial_distance, self.max_time = get_kwarg_item(kwargs, "initial_distance", 0), get_kwarg_item(kwargs,
                                                                                                             "max_time",
                                                                                                             0)
        self.has_max_time = kwargs.get("max_time") is not None

        # Adding the initial_distance, so it that is the height of the parabola
        self.set_all_variables(self.height_of_path + self.initial_distance, self.time, self.initial_distance)

    def run(self, is_reset_event, is_start_event, is_using_everything=False, is_changing_coordinates=True):
        """ summary: runs the code for the game_object following the physics path

            params:
                is_reset_event: boolean; if True it will call reset()
                is_start_event: boolean; if True it will call start()
                is_using_everything: boolean; if True it will use both velocity and acceleration and if False will just use velocity

        """

        self.last_time = self.current_time

        # It should not be started again if it has already been started because starting puts the current_time back to 0
        if is_start_event and not self.is_started:
            self.start()

        if is_reset_event:
            self.reset()

        if self.is_started:
            self.current_time += VelocityCalculator.time

        can_change_coordinates = self.is_started and self.game_object is not None

        should_change_player_coordinates = can_change_coordinates and is_changing_coordinates

        self.last_delta_time = self.current_time - self.last_time

        # Decides if it is just using the velocity or both velocity and acceleration
        if should_change_player_coordinates and not is_using_everything:
            self.game_object.__dict__[self.attribute_modifying] += self.get_velocity_displacement()

        elif should_change_player_coordinates:
            self.game_object.__dict__[self.attribute_modifying] = self.get_distance(self.current_time)

    def start(self):
        """Starts the physics path"""

        self.is_started = True
        self.current_time = 0

    def reset(self):
        """Ends and reset the physics path"""

        self.is_started = False
        self.current_time = 0
        self.last_time = 0

    def set_initial_distance(self, initial_distance):
        """Sets the initial distance, so the height of the parabola is equal to the vertex"""

        self.initial_distance = initial_distance
        self.set_all_variables(self.initial_distance + self.height_of_path, self.time, self.initial_distance)

    def get_velocity_displacement(self):
        """returns: double; the displacement from velocity (the last_time - start_time)"""

        current_distance = self.initial_velocity * self.current_time
        last_distance = self.initial_velocity * self.last_time

        return current_distance - last_distance

    def get_acceleration_displacement(self):
        """returns: double; the distance from acceleration with gravity"""

        current_distance = 1 / 2 * self.acceleration * pow(self.current_time, 2)
        last_distance = 1 / 2 * self.acceleration * pow(self.last_time, 2)

        return current_distance - last_distance

    def get_total_displacement(self):
        """returns: double; the displacement from both velocity and acceleration"""

        return self.get_velocity_displacement() + self.get_acceleration_displacement()

    def get_acceleration_displacement_from_time(self, time):
        """returns: double; the displacement from acceleration at that time"""

        return 1 / 2 * self.acceleration * pow(time, 2)

    def get_final_velocity(self):
        """returns: double; the velocity from acceleration (assumes initial_velocity is 0)"""

        return self.acceleration * self.current_time

    def is_done(self, should_reset=False):
        """returns: boolean; if the path is finished (and if 'should_reset' it will reset it)"""

        return_value = self.current_time >= self.max_time and self.has_max_time

        if should_reset and return_value:
            self.reset()

        return return_value

    def has_finished(self):
        """returns: boolean; if the path has either not started or is done"""

        return not self.is_started or self.is_done()



