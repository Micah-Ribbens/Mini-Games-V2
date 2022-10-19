from base.lines import LineSegment, Point
from base.utility_functions import *
from base.velocity_calculator import VelocityCalculator


class SimplePath:
    """A simple path that doesn't care about length or height of the object"""

    lines = []
    last_point = None

    def __init__(self, start_point, other_points):
        """Initializes the object"""

        self.lines = []
        self.last_point = start_point

        for other_point in other_points:
            self.add_point(other_point)

    def add_point(self, point):
        """Adds the point to this path"""

        self.lines.append(LineSegment(self.last_point, point))
        self.last_point = point

    def get_y_coordinate(self, x_coordinate):
        """returns: double; the y_coordinate at that x_coordinate (MUST be a function though- one x to one y)"""

        y_coordinate = 0

        for line in self.lines:
            if line.contains_x_coordinate(x_coordinate):
                y_coordinate = line.get_y_coordinate(x_coordinate)
                break

        return y_coordinate

    def get_lines(self):
        """returns: List of LineSegment; the lines of this simple path"""

        return self.lines

    def get_first_line(self):
        """returns: Point; the first point of the simple path"""

        return self.get_lines()[0]

    def get_last_line(self):
        """returns: Point; the last point of the simple path"""

        last_index = len(self.get_lines()) - 1
        return self.get_lines()[last_index]

    def __str__(self):
        string = ""
        for x in range(len(self.lines)):
            string += f"{self.lines[x]} || "

        return string

    def is_moving_down(self, x_coordinate):
        """returns: boolean; if the slope is negative at this point"""

        return_value = None

        for line in self.lines:
            if line.contains_x_coordinate(x_coordinate):
                return_value = not line.slope_is_positive()

        return return_value


class VelocityPath:
    """A path that takes into account velocity"""

    velocity = 0
    x_coordinate_lines = []
    y_coordinate_lines = []
    last_end_time = 0

    times = []  # Stores the times that the get_coordinates() function was called
    total_time = 0
    last_point = None
    is_unending = False
    previous_time = 0

    def __init__(self, start_point, other_points, velocity):
        """Initializes the object"""

        self.velocity = velocity
        self.path_lines = []
        self.x_coordinate_lines = []
        self.y_coordinate_lines = []
        self.times = []

        self.last_point = start_point

        for point in other_points:
            self.add_point(point)

    def add_point(self, point):
        """Does some calculations to find the time from the start of the last point to the end of the parameter 'point'
        and then calls add_time_point() to add the point"""

        x_distance = abs(self.last_point.x_coordinate - point.x_coordinate)
        y_distance = abs(self.last_point.y_coordinate - point.y_coordinate)

        x_time = x_distance / self.velocity
        y_time = y_distance / self.velocity

        # Whichever one is greater is how long the object will take to travel that distance because it...
        # can't travel faster than one of its max velocities
        time_to_travel_distance = max_value(x_time, y_time)

        end_time = time_to_travel_distance + self.last_end_time

        self.add_time_point(point, end_time)

    def add_time_point(self, point, end_time):
        """Adds the point to the path using the end_time as the x_coordinate for the x and y coordinate lines"""

        x_coordinate_line = LineSegment(Point(self.last_end_time, self.last_point.x_coordinate),
                                        Point(end_time, point.x_coordinate))

        y_coordinate_line = LineSegment(Point(self.last_end_time, self.last_point.y_coordinate),
                                        Point(end_time, point.y_coordinate))

        self.x_coordinate_lines.append(x_coordinate_line)
        self.y_coordinate_lines.append(y_coordinate_line)
        self.last_end_time = end_time

        # The height for the path_line doesn't matter
        self.last_point = point

    def get_coordinates(self):
        """returns: [left_edge, top_edge] for that time"""

        # The time should only be increased if it was not called that cycle
        if self.previous_time != VelocityCalculator.time:
            self.total_time += VelocityCalculator.time
            self.previous_time = VelocityCalculator.time

        max_time = self.last_end_time

        if self.total_time > max_time and self.is_unending:
            self.total_time %= max_time

        return self._get_coordinates(self.total_time)

    def _get_coordinates(self, time):
        """returns: [x_coordinate, y_coordinate]; the coordinates at that time"""

        index = self.get_index_of_line(time)
        x_coordinate_line = self.x_coordinate_lines[index]
        y_coordinate_line = self.y_coordinate_lines[index]

        return [x_coordinate_line.get_y_coordinate(time), y_coordinate_line.get_y_coordinate(time)]

    def get_index_of_line(self, time):
        """returns: int; the index of the line that the path is currently on"""

        return_value = len(self.x_coordinate_lines) - 1

        for x in range(len(self.y_coordinate_lines)):
            y_coordinate_line: LineSegment = self.y_coordinate_lines[x]
            start_point = y_coordinate_line.start_point
            end_point = y_coordinate_line.end_point

            if time >= start_point.x_coordinate and time <= end_point.x_coordinate:
                return_value = x

        return return_value

    def set_time(self, time):
        """Sets the time to the provided 'time'- if it is greater than the max time it is reduced to a smaller time"""

        self.total_time = time % self.max_time

    @property
    def max_time(self):
        return self.last_end_time

    def __str__(self):
        string = ""
        for x in range(len(self.y_coordinate_lines)):
            y_coordinate_line = self.y_coordinate_lines[x]
            x_coordinate_line = self.x_coordinate_lines[x]

            string += f"x {x_coordinate_line}, y {y_coordinate_line}\n"

        return string

class ActionPath(VelocityPath):
    """A path that performs an action at each of the points"""

    actions = []
    is_unending = True
    index_of_last_line = None
    object_on_path = None

    def __init__(self, start_point, object_on_path, velocity):
        """Initializes the object"""

        super().__init__(start_point, [], velocity)
        self.object_on_path = object_on_path
        self.actions = []

    def add_point(self, point, action, additional_time=None):
        """Adds the point ot the action path"""

        if additional_time is None:
            super().add_point(point)

        if additional_time is not None:
            super().add_time_point(point, self.last_end_time + additional_time)

        self.actions.append(action)

    def run(self):
        """Runs all the code for the action path"""

        new_index = self.get_index_of_line(self.total_time % self.max_time)

        if new_index != self.index_of_last_line:
            self.index_of_last_line = new_index
            self.actions[new_index]()

        self.object_on_path.left_edge, self.object_on_path.top_edge = self.get_coordinates()