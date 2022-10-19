import pygame

from base.dimensions import Dimensions
from base.events import Event
from base.utility_classes import HistoryKeeper
from base.utility_functions import *
from base.velocity_calculator import VelocityCalculator
from games.platformers.base.gravity_engine import GravityEngine
from games.platformers.base.player import Player
from games.platformers.platformer_screen import PlatformerScreen
from base.important_variables import *
from gui_components.grid import Grid
from gui_components.text_box import TextBox
from base.colors import *


class GeneratorTestScreen(PlatformerScreen):
    """A screen that is used for testing the generator"""

    screen_number_field = None
    platform_type_field = None
    generation_difficulty_field = None
    main_platform_number_field = None
    main_platforms = []
    hardest_platforms = []
    easiest_platforms = []
    current_index = 0
    is_hard_platform = True
    hud = None
    time = 0
    has_started = False

    increase_main_platform_number_event = None
    decrease_main_platform_number_event = None
    change_is_hard_platform_event = None

    def __init__(self, screen_number, total_screens, generation_difficulty, main_platforms, hardest_platforms, easiest_platforms):
        """Initializes the object"""

        self.players = [Player(KEY_A, KEY_D, KEY_W, KEY_S, KEY_F)]
        self.gravity_engine = GravityEngine(self.players, self.players[0].jumping_path.acceleration)

        self.hardest_platforms, self.easiest_platforms = hardest_platforms, easiest_platforms
        self.main_platforms = main_platforms

        # Have to do this here, so I can put the player on the platform
        other_platform_list = self.hardest_platforms if self.is_hard_platform else self.easiest_platforms
        self.platforms = [self.main_platforms[self.current_index], other_platform_list[self.current_index]]

        for player in self.players:
            player.gravity_engine = self.gravity_engine
            player.left_edge = self.platforms[0].left_edge + 10
            player.base_top_edge = self.platforms[0].top_edge - player.height
            player.set_top_edge(player.base_top_edge)

        self.screen_number_field = TextBox(f"Screen Number {screen_number} of {total_screens}", 20, False, purple, white)
        self.platform_type_field = TextBox("", 20, False, medium_green, white)
        self.generation_difficulty_field = TextBox(f"Generation Difficulty: {generation_difficulty}", 20, False, black, white)
        self.main_platform_number_field = TextBox("", 20, False, blue, white)

        self.increase_main_platform_number_event = Event()
        self.decrease_main_platform_number_event = Event()
        self.change_is_hard_platform_event = Event()

        self.hud = [self.screen_number_field, self.platform_type_field, self.generation_difficulty_field, self.main_platform_number_field]
        grid = Grid(Dimensions(0, 0, screen_length, screen_height * .1), None, 1, True)
        grid.turn_into_grid(self.hud, None, None)

    def run(self):
        """Runs all that is necessary to have a generator test screen"""

        super().run()
        other_platform_list = self.hardest_platforms if self.is_hard_platform else self.easiest_platforms
        self.platforms = [self.main_platforms[self.current_index], other_platform_list[self.current_index]]
        HistoryKeeper.add(self.players[0], self.players[0].name, needs_dimensions_only=True)
        # Changeable keys
        self.increase_main_platform_number_event.run(key_is_pressed(KEY_UP))
        self.decrease_main_platform_number_event.run(key_is_pressed(KEY_DOWN))
        self.change_is_hard_platform_event.run(key_is_pressed(pygame.K_SPACE))

        self.main_platform_number_field.text = f"Main Platform #{self.current_index + 1}"
        self.platform_type_field.text = "Showing Hard Platform" if self.is_hard_platform else "Is Showing Easy Platform"

        if self.decrease_main_platform_number_event.is_click():
            self.current_index = get_prev_index(self.current_index, len(self.main_platforms) - 1)

        if self.increase_main_platform_number_event.is_click():
            self.current_index = get_next_index(self.current_index, len(self.main_platforms) - 1)

        if self.change_is_hard_platform_event.is_click():
            self.is_hard_platform = not self.is_hard_platform

        # If the platforms were changed then the game should be reset
        if self.decrease_main_platform_number_event.is_click() or self.increase_main_platform_number_event.is_click():
            self.reset_game()

    def get_components(self):
        """returns: Component[]; all the components that should be ran and rendered"""

        return self.hud + self.platforms + self.players

    def reset_game(self):
        """Resets the game after the player's death"""

        for player in self.players:
            player.left_edge = self.main_platforms[self.current_index].left_edge
            player.base_top_edge = self.main_platforms[self.current_index].top_edge - player.height
            player.set_top_edge(player.base_top_edge)
            player.reset()

        HistoryKeeper.reset()
        self.gravity_engine.reset()
        self.frames = 0
        self.has_started = False

    def setup(self):
        self.reset_game()

