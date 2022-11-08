from games.platformer.powerups.powerup import Powerup
from games.platformer.weapons.bouncy_projectile_thrower import BouncyProjectileThrower


class BouncyProjectilePowerup(Powerup):
    """The powerup for attaining the bouncy projectile shooter"""

    def __init__(self, left_edge, top_edge):
        """Initializes the object"""

        super().__init__(left_edge, top_edge, "games/platformer/images/bouncy_gun.png")

    def run_player_collision(self, player):
        """Gives the player the bouncy projectile shooter"""

        player.set_weapon(BouncyProjectileThrower)