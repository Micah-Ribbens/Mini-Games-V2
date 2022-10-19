from gui_components.navigation_screen import NavigationScreen
from games.bird_shooter.bird_shooter_screen import BirdShooterScreen
from games.no_internet_game.no_internet_game_screen import NoInternetGameScreen
from games.space_shooter.space_shooter_screen import SpaceShooterScreen
from games.platformer.platformer_screen import PlatformerScreen
from gui_components.screen import Screen


class MainScreen(NavigationScreen):
    screen_names = ["Bird Shooter", "No Internet Game", "Space Shooter", "Platformer"]
    screens = [BirdShooterScreen(), NoInternetGameScreen(), SpaceShooterScreen(), PlatformerScreen()]

    def __init__(self):
        super().__init__(self.screen_names, self.screens)