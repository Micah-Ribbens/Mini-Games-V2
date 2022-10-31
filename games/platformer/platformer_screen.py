import random
from base.dimensions import Dimensions
from base.engines import CollisionsEngine
from base.file_reader import FileReader
from base.history_keeper import HistoryKeeper
from base.lines import Point
from base.paths import SimplePath
from base.utility_functions import is_within_screen
from base.velocity_calculator import VelocityCalculator
from game_dependencies.platformer.generator import Generator
from game_dependencies.platformer.gravity_engine import GravityEngine
from games.platformer.inanimate_objects.platform import Platform
from games.platformer.players.player import Player
from games.platformer.enemies.charging_bull import ChargingBull
from games.platformer.enemies.straight_ninja import StraightEnemy
from games.platformer.enemies.bouncy_ninja import BouncyEnemy
from gui_components.grid import Grid
from game_dependencies.platformer.health_bar import HealthBar
from gui_components.hud import HUD
from gui_components.screen import Screen
from base.important_variables import *
from game_dependencies.platformer.platformer_variables import *
from games.platformer.weapons.bouncy_projectile_thrower import BouncyProjectile


class PlatformerScreen(Screen):
    """A basic platformer game"""
    players = []
    player_health_bars = []
    enemies = []
    platforms = []
    game_objects = []
    gravity_engine = None
    frames = 0
    last_time = 0  # The last that objects were added to the History Keeper
    rightmost_platform = None
    generator = None

    # Modifiable Numbers
    health_grid_length = VelocityCalculator.get_measurement(screen_length, 25)
    health_grid_height = VelocityCalculator.get_measurement(screen_height, 10)

    hud_length = screen_length - health_grid_length
    hud_height = VelocityCalculator.get_measurement(screen_height, 6)
    hud = HUD(1, [], hud_length, hud_height, 1, None)

    # Scoring
    player_score = 0
    high_score = 0
    score_to_difficulty = SimplePath(Point(0, 50), [Point(1000, 70), Point(2500, 90), Point(5000, 100),
                                                    Point(float("inf"), 100)])

    def __init__(self):
        """Initializes the object"""

        super().__init__("games/platformer/images/background_faded.png")

        file_reader = FileReader("games\\platformer\\high_scores.txt")
        self.high_score = int(file_reader.get_float_list("high_score")[0])

        health_grid = Grid(Dimensions(0, 0, self.health_grid_length, self.health_grid_height), 2, 2)
        self.players = [Player(KEY_A, KEY_D, KEY_W, KEY_S, KEY_F)]
        self.setup_enemies_and_platforms()
        self.gravity_engine = GravityEngine(self.players, self.players[0].jumping_path.acceleration)

        for player in self.players:
            player.gravity_engine = self.gravity_engine
            player.left_edge = self.platforms[0].left_edge + 10
            player.base_top_edge = self.platforms[0].top_edge - player.height
            player.set_top_edge(player.base_top_edge)

            self.player_health_bars.append(HealthBar(player, lambda: False))

        health_grid.turn_into_grid(self.player_health_bars, None, None)
        self.generator = Generator(self.players[0])
        self.hud.set_dimensions(health_grid.dimensions.right_edge, 0, self.hud_length, self.hud_height)

    def setup_enemies_and_platforms(self):
        """Creates the enemies and platforms of the game for starting out"""

        # Platform above you
        # self.platforms = [Platform(), Platform(Platform().x_coordinate, Platform().y_coordinate - self.players[0].max_jump_height * 1/2 - 200 - self.players[0].height, screen_length, 200, True)]

        # Two normal platforms
        # self.platforms = [Platform(), Platform(Platform().right_edge + 200, Platform().y_coordinate - self.players[0].max_jump_height, 200, 200, True)]

        # One Long Platform
        self.platforms = [Platform(0, screen_height - 100, 800, 100)]

        # Sandwich Platform
        # self.platforms = [Platform(100, 300, 800, 100), Platform(0, 200, 100, 100), Platform(910, 200, 100, 100)]

        # One Medium Platform
        # self.platforms = [Platform(100, 300, 800, 100, True)]

        self.enemies = []

        self.update_rightmost_platform()

    def run(self):
        """Runs all the code necessary in order for the platformer to work"""

        self.high_score = max(self.player_score, self.high_score)
        self.hud.update([self.player_score], self.high_score)
        self.gravity_engine.run()
        for player in self.players:
            # Have to do this every cycle so the player is realisticly affected by gravity every cycle
            if player.platform_is_on is not None and not CollisionsEngine.is_collision(player, player.platform_is_on):
                player.set_is_on_platform(False, None)

        if self.frames % 1 == 0 and self.frames > 1:
            self.update_game_objects()
            self.run_all_collisions()

            # All the enemies and players should do something based on the updated collision they got from 'self.run_all_collisions()'
            for game_object in self.enemies + self.players:
                game_object.run_collisions(self.last_time)

        if self.frames % 1 == 0:
            self.add_game_objects()
            self.last_time = VelocityCalculator.time

        for enemy in self.enemies:
            enemy.run_player_interactions(self.players)

        self.frames += 1

        self.run_side_scrolling()
        self.run_platform_generation()

    def run_platform_generation(self):
        """Runs all the code for generating platforms"""

        if self.rightmost_platform.right_edge <= screen_length:
            difficulty = self.score_to_difficulty.get_y_coordinate(self.player_score)
            new_platform = self.generator.generate_platform(self.rightmost_platform, difficulty)
            self.platforms.append(new_platform)
            new_enemy = self.get_random_enemy(new_platform)
            self.enemies.append(new_enemy)
            self.update_rightmost_platform()
            self.gravity_engine.add_game_objects([new_enemy])

    def get_random_enemy(self, platform):
        """returns: Enemy; a random enemy"""

        enemy_types = [StraightEnemy, ChargingBull, BouncyEnemy]
        enemy_type = random.choice(enemy_types)
        return ChargingBull(10, 20, platform)

    def run_side_scrolling(self):
        """Makes the screen side scroll based off the player who is the farthest behind"""

        # First the players are sorted by the smallest left_edge and then the smallest player is taken
        farthest_back_player = list(sorted(self.players, key=lambda player: player.left_edge))[0]
        shortest_distance = farthest_back_player.right_edge

        # If the distance of the farthest back player is greater than the distance needed for sidescrolling then
        # All the objects in the game should be side scrolled
        if shortest_distance > side_scrolling_start_distance:
            side_scrolling_distance = shortest_distance - side_scrolling_start_distance

            self.side_scroll_objects(side_scrolling_distance, self.players)
            self.side_scroll_objects(side_scrolling_distance, self.enemies)
            self.side_scroll_objects(side_scrolling_distance, self.platforms)

    def side_scroll_objects(self, distance, game_objects):
        """Moves all the objects leftwards by the distance specified (side scrolling)"""

        for game_object in game_objects:
            game_object.update_for_side_scrolling(distance)

    def update_game_objects(self):
        """Runs the necessary code to prepare for collisions and some other miscellaneous stuff like making sure
        killed enemies are not put onto the screen and resetting the game if the player dies"""

        player_components = []
        for player in self.players:
            if player.hit_points_left <= 0 or not is_within_screen(player):
                self.reset_game()

            player_components += player.get_sub_components()
            player.reset_collision_data()

        updated_enemies = []
        enemy_components = []
        for enemy in self.enemies:
            enemy.reset_collision_data()

            if enemy.hit_points_left <= 0:
                self.player_score += score_from_killing_enemy

            if enemy.hit_points_left > 0 and enemy.platform.right_edge >= 0:
                updated_enemies.append(enemy)
                enemy_components += enemy.get_sub_components()

        updated_platforms = []
        for platform in self.platforms:
            if platform.right_edge >= 0:
                updated_platforms.append(platform)

            else:
                self.player_score += score_from_passing_platform

        self.platforms = updated_platforms

        self.enemies = updated_enemies
        self.game_objects = player_components + enemy_components + self.platforms

    def update_rightmost_platform(self):
        """Updates the attribute 'rightmost_platform' so it is actually the rightmost_platform"""

        # First the platforms are sorted with right_edge's decreasing, then the index of 0 is taken giving the rightmost platform
        self.rightmost_platform = list(sorted(self.platforms, key=lambda platform: platform.right_edge, reverse=True))[0]

    def reset_game(self):
        """Resets the game after the player's death"""

        for player in self.players:
            player.reset()

        self.setup_enemies_and_platforms()
        self.gravity_engine.reset()
        HistoryKeeper.last_objects = {}
        self.frames = 0
        self.player_score = 0

    def run_all_collisions(self):
        """Runs all the collisions between the player, projectiles, and enemies"""

        # TODO maybe could make this quicker, but not sure if it is worth it
        for i in range(len(self.game_objects)):
            object1 = self.game_objects[i]
            # Only the objects that can be added to the History Keeper should be checked for a collision; also
            # The platforms don't need to check to see if they collided with other objects because if something
            # Collides with the platform it won't do anything in reaction
            if not object1.is_addable or self.is_platform(object1):
                continue

            for j in range(len(self.game_objects)):
                object2 = self.game_objects[j]

                collision_is_possible = object2.is_addable and len(object1.object_type) != len(object2.object_type)

                if collision_is_possible and CollisionsEngine.is_collision(object1, object2):
                    self.run_object_collisions(object1, object2)

    def run_object_collisions(self, main_object, other_object):
        """Runs the collisions between the 'main_object' and the 'other_object;' the main_object acts upon the other_object.
        By act upon I mean damages the other_object, moves the other_object, etc."""

        self.run_user_weapon_inanimate_collisions(self.is_player_weapon(main_object), self.is_player(main_object), main_object, other_object)
        self.run_user_weapon_inanimate_collisions(self.is_enemy_weapon(main_object), self.is_enemy(main_object), main_object, other_object)

        if self.is_enemy(main_object) and self.is_player(other_object):
            main_object.run_enemy_collision(other_object, main_object.index)

        if self.is_enemy_weapon(main_object) and self.is_player(other_object):
            main_object.user.run_enemy_collision(other_object, main_object.index)

        if self.is_enemy_weapon(main_object) and self.is_platform(other_object):
            main_object.user.run_inanimate_object_collision(other_object, main_object.index, self.last_time)

        if self.is_player_weapon(main_object) and self.is_enemy(other_object):
            main_object.user.run_enemy_collision(other_object, main_object.index)

        # Doing it this way, so a collision does not happen twice - once when the player_weapon is the main_object
        # And the other where the enemy_weapon is the main_object.
        if self.is_player_weapon(main_object) and self.is_enemy_weapon(other_object):
            main_object.user.run_enemy_collision(other_object, main_object.index)

        if self.is_enemy_weapon(main_object) and self.is_enemy_weapon(other_object):
            main_object.user.run_enemy_collision(other_object, main_object.index)

    def run_user_weapon_inanimate_collisions(self, is_weapon, is_user, user_or_weapon, other_object):
        """Runs the collisions between the user + the user's weapon and inanimate objects"""

        if is_user and self.is_platform(other_object):
            user_or_weapon.run_inanimate_object_collision(other_object, user_or_weapon.index, self.last_time)

        if is_weapon and self.is_platform(other_object):
            user_or_weapon.user.run_inanimate_object_collision(other_object, user_or_weapon.index, self.last_time)

    def add_game_objects(self):
        """Adds all the game objects to the HistoryKeeper"""

        for player in self.players:
            self.add_sub_components(player.get_sub_components())

        self.add_sub_components(self.platforms)

        for enemy in self.enemies:
            self.add_sub_components(enemy.get_sub_components())

    def add_sub_components(self, component_list):
        """Adds all the components in the component_list to the History Keeper"""

        for component in component_list:
            if component.is_addable:
                component.name = id(component)
                # TODO figure out why needs_dimensions does not work
                HistoryKeeper.add(component, component.name, needs_deepcopy=True)

    def run_on_close(self):
        """Runs what should happen when the game is closed (save the high scores)"""

        file = open("games/platformer/high_scores.txt", "w+")
        file.write(f"high_scores:[{self.high_score}]")
        file.close()

    def get_components(self):
        """returns: Component[]; all the components that should be rendered"""

        components = []
        for game_object in self.players + self.enemies:
            components += game_object.get_components()

        return [self.hud] + components + self.player_health_bars + self.platforms

    # HELPER METHODS FOR COLLISIONS; Since they all have a unique length I can just use the lengths here
    def is_enemy(self, game_object):
        """returns: boolean; if the game_object is just an enemy (not a weapon) --> object type would be 'Enemy'"""

        return len(game_object.object_type) == 5

    def is_enemy_weapon(self, game_object):
        """returns: boolean; if the game_object is an enemy's weapon --> object type would be 'Enemy Weapon'"""

        return len(game_object.object_type) == 12

    def is_player(self, game_object):
        """returns: boolean; if the game_object is the player --> object type would be 'Player'"""

        return len(game_object.object_type) == 6

    def is_player_weapon(self, game_object):
        """returns: boolean; if the game_object is the player's weapon --> object type would be 'Player Weapon'"""

        return len(game_object.object_type) == 13

    def is_platform(self, game_object):
        """returns: boolean; if the game_object is a platform --> object type would be 'Platform'"""

        return len(game_object.object_type) == 8








