from games.platformer.powerups.powerup import Powerup
from game_dependencies.platformer.platformer_variables import health_increase_from_heart


class HeartPowerup(Powerup):
    """The powerup for giving the player more health"""

    def __init__(self, left_edge, top_edge):
        """Initializes the object"""

        super().__init__(left_edge, top_edge, "games/platformer/images/heart.png")

    def run_player_collision(self, player):
        """Gives the player more health"""

        player.increase_health(health_increase_from_heart)