from games.platformer.enemies.straight_ninja import StraightEnemy
from games.platformer.weapons.bouncy_projectile_thrower import BouncyProjectileThrower
from game_dependencies.platformer.platformer_variables import player_height


class BouncyEnemy(StraightEnemy):
    """A ninja that throws projectiles that bounce"""

    def __init__(self, damage, hit_points, platform):
        """Initializes the object"""

        super().__init__(damage, hit_points, platform, "games/platformer/images/bouncy_tank.png")
        self.weapon = BouncyProjectileThrower(lambda: False, self)

    @property
    def projectile_height(self):
        # Since all players should be the same height, then the first one can be safely chosen
        # because there has to be at least one player
        return player_height / 2
