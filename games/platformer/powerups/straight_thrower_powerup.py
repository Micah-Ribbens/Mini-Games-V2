from games.platformer.powerups.powerup import Powerup
from games.platformer.weapons.straight_projectile_thrower import StraightProjectileThrower


class StraightProjectilePowerup(Powerup):
    """The powerup for attaining the straight projectile shooter"""

    def __init__(self, left_edge, top_edge):
        """Initializes the object"""

        super().__init__(left_edge, top_edge, "games/platformer/images/straight_gun.png")

    def run_player_collision(self, player):
        """Gives the player the straight projectile shooter"""

        player.set_weapon(StraightProjectileThrower)