import os

from base.colors import *
from base.file_reader import FileReader
from gui_components.navigation_screen import NavigationScreen
from games.space_shooter.meteorite_game_screen import MeteoriteGameScreen
from gui_components.text_box import TextBox
from base.important_variables import *
from gui_components.screen import Screen


class SpaceShooterScreen(NavigationScreen):
    meteorite_game_screens = [MeteoriteGameScreen(1, False), MeteoriteGameScreen(2, False), MeteoriteGameScreen(2, True)]

    def __init__(self):
        super().__init__(["Single Player", "2 Player Co-op", "2 Player Versus"], self.meteorite_game_screens)
        self.modify_values(purple, KEY_Q)

        file_reader = FileReader("games/space_shooter/high_score.txt")
        high_scores = file_reader.get_float_list("high_scores")

        for x in range(len(self.meteorite_game_screens)):
            self.meteorite_game_screens[x].high_score = int(high_scores[x])

    def run_on_close(self):
        """Saves the high score"""

        high_scores = []

        for screen in self.meteorite_game_screens:
            high_scores.append(screen.high_score)

        high_score_string = high_scores.__str__().replace(" ", "")
        file_writer = open("games/space_shooter/high_score.txt", "w+")
        file_writer.write(f"high_scores:{high_score_string}")
