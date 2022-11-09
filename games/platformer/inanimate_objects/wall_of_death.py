from base.events import TimedEvent
from base.important_variables import *
from game_dependencies.platformer.game_object import GameObject
from gui_components.component import Component
from base.velocity_calculator import VelocityCalculator
from game_dependencies.platformer.platformer_constants import TIME_BEFORE_WALL_OF_DEATH_STARTS_MOVING, TIME_GAME_HAS_RUN_TO_WALL_OF_DEATH_VELOCITY


class WallOfDeath(Component, GameObject):
    """The wall that follows after the player and if the player touches it they die"""

    total_time = 0
    delayed_start_timed_event = TimedEvent(TIME_BEFORE_WALL_OF_DEATH_STARTS_MOVING)
    velocity = 0

    def __init__(self):
        """Initializes the object"""

        super().__init__("games/platformer/images/wall_of_death.png")
        self.delayed_start_timed_event.start()
        self.number_set_dimensions(-screen_length, 0, screen_length, screen_height)

    def run(self):
        """Makes the wall of death follow after the player and how fast it moves depends on how long the game has run"""

        if self.delayed_start_timed_event.has_finished():
            self.total_time += VelocityCalculator.time
            self.velocity = TIME_GAME_HAS_RUN_TO_WALL_OF_DEATH_VELOCITY.get_y_coordinate(self.total_time)
            self.left_edge += VelocityCalculator.calculate_distance(self.velocity)

        else:
            self.delayed_start_timed_event.run(False, False)

    def reset(self):
        """Resets the wall of death, so it is exactly like it is at the start of the game"""

        self.delayed_start_timed_event.start()
        self.total_time = 0
        self.number_set_dimensions(-screen_length, 0, screen_length, screen_height)
