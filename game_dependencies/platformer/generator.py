# TODO make sure to add the new generated platforms and maybe other stuff to the History Keeper, so collisions can happen
import random

from base.lines import Point
from base.important_variables import screen_height, screen_length
from base.paths import SimplePath
from base.velocity_calculator import VelocityCalculator
from games.platformer.inanimate_objects.platform import Platform
from games.platformer.players.player import Player
from game_dependencies.platformer.platformer_constants import *


class Generator:
    """Generates platforms, enemies, and other things semi-randomly (as long as it is playable for the player and mantains a good difficulty)"""

    # Modifiable Numbers
    player = None

    def __init__(self, player):
        self.player = player

    # Functions that game uses (aren't just for tests)
    def _get_accuracy(self, difficulty):
        """returns: double; how accurate the player has to be (1 - margin_of_error)"""

        # Margins_of_error are in percentages
        return 1 - ( MARGINS_OF_ERROR.get_y_coordinate(difficulty) / 100 )

    def _get_bottommost_top_edge(self, last_platform, platform_height):
        """returns: double; the generated platform's bottommost top_edge (must stay within the screen)"""

        return_value = last_platform.top_edge + MAX_VERTICAL_CHANGE

        # The platform's bottom must be visible
        if return_value + platform_height >= screen_height:
            return_value = screen_height - platform_height

        return return_value

    def get_platform_within_screen(self, last_platform: Platform, next_platform: Platform):
        """ returns: Platform; the updated 'platform' that is within the screen meaning when the player gets to the edge
            of 'last_platform' they can see a good amount of the next platform"""

        last_platform_length_left = last_platform.right_edge - SIDE_SCROLLING_START_DISTANCE

        next_platform_length_visible = screen_length - next_platform.left_edge
        # Have to add that because side scrolling will increase how much of the platform is visible
        next_platform_length_visible += last_platform_length_left

        if next_platform_length_visible < MINIMUM_PLATFORM_LENGTH_VISIBLE:
            difference = MINIMUM_PLATFORM_LENGTH_VISIBLE - next_platform_length_visible
            next_platform.left_edge -= difference

        return next_platform

    def generate_platform(self, last_platform, difficulty):
        """returns: Platform; the next platform, which would be after 'last_platform;' uses the difficulty to decide how hard of a jump it should be"""

        accuracy = self._get_accuracy(difficulty)
        new_platform_height = random.randint(MINIMUM_PLATFORM_HEIGHT, MAXIMUM_PLATFORM_HEIGHT)

        topmost_top_edge = self.player.get_topmost_top_edge(last_platform, accuracy, self._get_accuracy(1))
        bottommost_top_edge = self._get_bottommost_top_edge(last_platform, new_platform_height)
        new_platform_top_edge = random.randint(int(topmost_top_edge), int(bottommost_top_edge))

        new_platform_length = random.randint(MINIMUM_PLATFORM_LENGTH, MAXIMUM_PLATFORM_LENGTH)

        max_vertical_time = self.player.get_max_time_to_top_edge(last_platform.top_edge, new_platform_top_edge)

        max_distance = self.get_horizontal_distance(max_vertical_time, accuracy)
        min_distance = self.get_horizontal_distance(max_vertical_time, accuracy - MINIMUM_GENERATOR_ACCURACY_DECREASE)
        distance = random.randint(int(min_distance), int(max_distance))

        new_platform_left_edge = last_platform.right_edge + distance
        platform = Platform(new_platform_left_edge, new_platform_top_edge, new_platform_length, new_platform_height)

        return self.get_platform_within_screen(last_platform, platform)

    def get_horizontal_distance(self, vertical_time, accuracy):
        """returns: double; the horizontal distance apart the old platform and the new one should be"""

        # 2 * player's length because one of them comes from the player not being affected by gravity until its
        # left_edge > the last platform's right edge and other one because they can land on the new platform when
        # the right_edge is > the new platform's left_edge
        return vertical_time * PLAYER_MAX_HORIZONTAL_VELOCITY * accuracy + PLAYER_LENGTH * 2

    # Just for tests
    def get_hardest_platform(self, last_platform, difficulty):
        """returns: Platform; the hardest platform possible at this difficulty"""

        accuracy = self._get_accuracy(difficulty)
        platform_height = random.randint(MINIMUM_PLATFORM_HEIGHT, MAXIMUM_PLATFORM_HEIGHT)

        platform_top_edge = self.player.get_topmost_top_edge(last_platform, accuracy, self._get_accuracy(1))

        platform_length = random.randint(MINIMUM_PLATFORM_LENGTH, MAXIMUM_PLATFORM_LENGTH)

        max_vertical_time = self.player.get_max_time_to_top_edge(last_platform.top_edge, platform_top_edge)

        platform_left_edge = last_platform.right_edge + self.get_horizontal_distance(max_vertical_time, accuracy)

        platform = Platform(platform_left_edge, platform_top_edge, platform_length, platform_height)

        return self.get_platform_within_screen(last_platform, platform)

    def get_easiest_platform(self, last_platform, difficulty):
        """returns: Platform; the easiest platform possible at this difficulty"""

        accuracy = self._get_accuracy(difficulty)
        platform_height = random.randint(MINIMUM_PLATFORM_HEIGHT, MAXIMUM_PLATFORM_HEIGHT)
        platform_top_edge = self._get_bottommost_top_edge(last_platform, platform_height)

        platform_length = random.randint(MINIMUM_PLATFORM_LENGTH, MAXIMUM_PLATFORM_LENGTH)

        max_vertical_time = self.player.get_max_time_to_top_edge(last_platform.top_edge, platform_top_edge)
        platform_left_edge = last_platform.right_edge + self.get_horizontal_distance(max_vertical_time, accuracy)

        if platform_left_edge + platform_length > screen_length:
            platform_left_edge = screen_length - platform_length

        return Platform(platform_left_edge, platform_top_edge, platform_length, platform_height)




