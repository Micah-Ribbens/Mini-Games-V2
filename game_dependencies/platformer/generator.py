# TODO make sure to add the new generated platforms and maybe other stuff to the History Keeper, so collisions can happen
import random

from base.lines import Point
from base.important_variables import screen_height, screen_length
from base.paths import SimplePath
from base.velocity_calculator import VelocityCalculator
from games.platformer.inanimate_objects.platform import Platform
from games.platformer.players.player import Player
from game_dependencies.platformer.platformer_variables import *


class Generator:
    """Generates platforms, enemies, and other things semi-randomly (as long as it is playable for the player and mantains a good difficulty)"""

    # Modifiable Numbers
    max_y_change = VelocityCalculator.get_measurement(screen_height, 25)
    min_platform_height = int(VelocityCalculator.get_measurement(screen_height, 10))
    max_platform_height = int(VelocityCalculator.get_measurement(screen_height, 20))
    min_platform_length = int(VelocityCalculator.get_measurement(screen_length, 30))
    max_platform_length = int(VelocityCalculator.get_measurement(screen_length, 45))
    min_distance_accuracy_decrease = .05
    player = None

    def __init__(self, player):
        self.player = player

    def generate_platform(self, last_platform, difficulty):
        """returns: Platform; the next platform, which would be after 'last_platform;' uses the difficulty to decide how hard of a jump it should be"""

        accuracy = self._get_accuracy(difficulty)
        new_platform_height = random.randint(int(self.min_platform_height), int(self.max_platform_height))

        topmost_top_edge = self.player.get_topmost_top_edge(last_platform, accuracy, self._get_accuracy(1))
        bottommost_top_edge = self._get_bottommost_top_edge(last_platform, new_platform_height)
        new_platform_top_edge = random.randint(int(topmost_top_edge), int(bottommost_top_edge))

        new_platform_length = random.randint(int(self.min_platform_length), int(self.max_platform_length))

        max_vertical_time = self.player.get_max_time_to_top_edge(last_platform.top_edge, new_platform_top_edge)

        max_distance = self.get_horizontal_distance(max_vertical_time, accuracy)
        min_distance = self.get_horizontal_distance(max_vertical_time, accuracy - self.min_distance_accuracy_decrease)
        distance = random.randint(int(min_distance), int(max_distance))

        new_platform_left_edge = last_platform.right_edge + distance
        platform = Platform(new_platform_left_edge, new_platform_top_edge, new_platform_length, new_platform_height)

        return self.get_platform_within_screen(last_platform, platform)

    def get_horizontal_distance(self, vertical_time, accuracy):
        """returns: double; the horizontal distance apart the old platform and the new one should be"""

        # 2 * player's length because one of them comes from the player not being affected by gravity until its
        # x coordinate > the last platform's right edge and other one because they can land on the new platform when
        # the right edge is > the new platform's x coordinate
        return vertical_time * self.player.max_velocity * accuracy + self.player.length * 2

    def get_hardest_platform(self, last_platform, difficulty):
        """returns: Platform; the hardest platform possible at this difficulty"""

        accuracy = self._get_accuracy(difficulty)
        platform_height = random.randint(int(self.min_platform_height), int(self.max_platform_height))

        platform_top_edge = self.player.get_topmost_top_edge(last_platform, accuracy, self._get_accuracy(1))

        platform_length = random.randint(int(self.min_platform_length), int(self.max_platform_length))

        max_vertical_time = self.player.get_max_time_to_top_edge(last_platform.top_edge, platform_top_edge) * accuracy

        # 2 * player's length because one of them comes from the player not being affected by gravity until its
        # x coordinate > the last platform's right edge and other one because they can land on the new platform when
        # the right edge is > the new platform's x coordinate
        platform_left_edge = last_platform.right_edge + self.get_horizontal_distance(max_vertical_time, accuracy)

        platform = Platform(platform_left_edge, platform_top_edge, platform_length, platform_height)

        return self.get_platform_within_screen(last_platform, platform)

    def get_platform_within_screen(self, last_platform: Platform, next_platform: Platform):
        """ returns: Platform; the updated 'platform' that is within the screen meaning when the player gets to the edge
            of 'last_platform' they can see a good amount of the next platform"""

        last_platform_length_left = last_platform.right_edge - side_scrolling_start_distance - self.player.length

        next_platform_length_visible = screen_length - next_platform.left_edge
        next_platform_length_visible += last_platform_length_left

        if next_platform_length_visible < min_platform_length_visible:
            difference = min_platform_length_visible - next_platform_length_visible
            next_platform.left_edge -= difference

        return next_platform

    def get_easiest_platform(self, last_platform, difficulty):
        """returns: Platform; the easiest platform possible at this difficulty"""

        accuracy = self._get_accuracy(difficulty)
        platform_height = random.randint(int(self.min_platform_height), int(self.max_platform_height))
        platform_top_edge = self._get_bottommost_top_edge(last_platform, platform_height)

        platform_length = random.randint(int(self.min_platform_length), int(self.max_platform_length))

        max_vertical_time = self.player.get_max_time_to_top_edge(last_platform.top_edge, platform_top_edge)
        platform_left_edge = last_platform.right_edge + self.get_horizontal_distance(max_vertical_time, accuracy)

        if platform_left_edge + platform_length > screen_length:
            platform_left_edge = screen_length - platform_length

        return Platform(platform_left_edge, platform_top_edge, platform_length, platform_height)

    def _get_accuracy(self, difficulty):
        """returns: double; how accurate the player has to be (1 - margin_of_error)"""

        margins_of_error = SimplePath(Point(0, 35))
        margins_of_error.add_point(Point(20, 30))
        margins_of_error.add_point(Point(40, 25))
        margins_of_error.add_point(Point(60, 20))
        margins_of_error.add_point(Point(70, 15))
        margins_of_error.add_point(Point(80, 10))
        margins_of_error.add_point(Point(90, 6))
        margins_of_error.add_point(Point(100, 0))

        # Margins_of_error are in percentages
        return 1 - ( margins_of_error.get_y_coordinate(difficulty) / 100 )

    def _get_bottommost_top_edge(self, last_platform, platform_height):
        """returns: double; the generated platform's bottommost top_edge (must stay within the screen)"""

        return_value = last_platform.top_edge + self.max_y_change

        # The platform's bottom must be visible
        if return_value + platform_height >= screen_height:
            return_value = screen_height - platform_height

        return return_value




