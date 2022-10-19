import cProfile

import pygame.display

from base.engines import CollisionsEngine
from base.path import *
from base.utility_classes import HistoryKeeper
from base.important_variables import *
import time
from base.velocity_calculator import VelocityCalculator
from games.platformers.base.generator import Generator
from games.platformers.base.platform import Platform
from games.platformers.platformer_screen import PlatformerScreen
from games.platformers.tests.generator_test_screen import GeneratorTestScreen
from gui_components.navigation_screen import NavigationScreen
from gui_components.screen import Screen


# TODO Make sure player's jump takes into account how much time has passed this cycle!!!
class GeneratorSelectorScreen(NavigationScreen):
    """The screen for testing the generator; this screen is for navigating between the different screens"""

    sub_screens = []

    def __init__(self):
        """Initializes the object"""

        generator = Generator()
        main_platforms = self.get_main_platforms()
        player = PlatformerScreen().players[0]
        total_screens = 100
        for x in range(total_screens):
            hardest_platforms = []
            easiest_platforms = []
            for main_platform in main_platforms:

                hardest_platforms.append(generator.get_hardest_platform(player, main_platform, x + 1))
                easiest_platforms.append(generator.get_easiest_platform(player, main_platform, x + 1))

            self.sub_screens.append(GeneratorTestScreen(x + 1, total_screens, x + 1, main_platforms, hardest_platforms, easiest_platforms))

        super().__init__(self.sub_screens, ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36', '37', '38', '39', '40', '41', '42', '43', '44', '45', '46', '47', '48', '49', '50', '51', '52', '53', '54', '55', '56', '57', '58', '59', '60', '61', '62', '63', '64', '65', '66', '67', '68', '69', '70', '71', '72', '73', '74', '75', '76', '77', '78', '79', '80', '81', '82', '83', '84', '85', '86', '87', '88', '89', '90', '91', '92', '93', '94', '95', '96', '97', '98', '99', '100'])

    def get_main_platforms(self):
        """returns: Platform[]; the main platforms the player will be jumping from to the generated platforms"""

        main_platform_left_edge = 0
        main_platform_length = 200
        main_platform_height = 100
        return [
            Platform(main_platform_left_edge, 200, main_platform_length, main_platform_height, True),
            Platform(main_platform_left_edge, 300, main_platform_length, main_platform_height, True),
            Platform(main_platform_left_edge, 400, main_platform_length, main_platform_height, True),
            Platform(main_platform_left_edge, 500, main_platform_length, main_platform_height, True),
            Platform(main_platform_left_edge, 600, main_platform_length, main_platform_height, True)
        ]


game_window.add_screen(GeneratorSelectorScreen())
total_frames = 0
total_time = 0

while True:
    start_time = time.time()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print(f"Average Frames {total_frames / total_time} Total Frames {total_frames} Total Time {total_time}")
            pygame.quit()

    game_window.run()

    CollisionsEngine.objects_to_data = {}
    function_runner.run()
    changer.run_changes()
    HistoryKeeper.last_time = VelocityCalculator.time
    VelocityCalculator.time = time.time() - start_time
    total_frames += 1
    total_time += VelocityCalculator.time



