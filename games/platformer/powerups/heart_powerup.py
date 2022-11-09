from games.platformer.powerups.powerup import Powerup
from game_dependencies.platformer.platformer_constants import HEALTH_INCREASE_FROM_HEART


class HeartPowerup(Powerup):
    """The powerup for giving the player more health"""

    def __init__(self, left_edge, top_edge):
        """Initializes the object"""

        super().__init__(left_edge, top_edge, "games/platformer/images/heart.png")

    def run_player_collision(self, player):
        """Gives the player more health"""

        player.increase_health(HEALTH_INCREASE_FROM_HEART)