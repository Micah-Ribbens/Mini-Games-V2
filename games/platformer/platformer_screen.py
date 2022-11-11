import random

from base.colors import *
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
from games.platformer.inanimate_objects.wall_of_death import WallOfDeath
from games.platformer.players.player import Player
from games.platformer.enemies.charging_bull import ChargingBull
from games.platformer.enemies.straight_enemy import StraightEnemy
from games.platformer.enemies.bouncy_enemy import BouncyEnemy
from gui_components.grid import Grid
from game_dependencies.platformer.health_bar import HealthBar
from gui_components.hud import HUD
from gui_components.intermediate_screen import IntermediateScreen
from gui_components.screen import Screen
from base.important_variables import *
from game_dependencies.platformer.platformer_constants import *
from games.platformer.powerups.ammo_powerup import AmmoPowerup
from games.platformer.powerups.heart_powerup import HeartPowerup
from games.platformer.powerups.straight_thrower_powerup import StraightProjectilePowerup
from games.platformer.powerups.bouncy_projectile_powerup import BouncyProjectilePowerup
from games.platformer.powerups.powerup import Powerup
from base.utility_functions import *

# TODO FIGURE OUT WHY SOMETIMES THERE ARE NO ENEMIES ON PLATFORM
from gui_components.text_box import TextBox


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
    number_of_platforms_generated = 0
    wall_of_death = WallOfDeath()
    intermediate_screen = IntermediateScreen()

    # Modifiable Numbers
    health_grid_length = VelocityCalculator.get_measurement(screen_length, 25)
    health_grid_height = VelocityCalculator.get_measurement(screen_height, 10)

    hud_length = screen_length - health_grid_length
    hud_height = VelocityCalculator.get_measurement(screen_height, 6)
    ammo_field = TextBox("Ammo Left:", 20, white, brown, True)
    hud = HUD(1, [ammo_field], hud_length, hud_height, 1, None)
    powerups = []

    # Scoring
    player_score = 0
    high_score = 0
    score_to_difficulty = SCORE_TO_GAME_DIFFICULTY
    is_high_score = False

    def __init__(self):
        """Initializes the object"""

        super().__init__("games/platformer/images/background_faded.png")

        file_reader = FileReader("games\platformer\high_scores.txt")
        self.high_score = int(file_reader.get_float_list("high_scores")[0])

        self.setup_enemies_and_platforms()
        self.setup_players()

    def setup_players(self):
        """Creates all the player's and all the necessary stuff associated with them (GravityEngine, HealthGrid, Generator, HUD)"""

        self.players = [Player(KEY_A, KEY_D, KEY_W, KEY_S, KEY_F)]
        self.gravity_engine = GravityEngine(self.players, self.players[0].jumping_path.acceleration)

        for player in self.players:
            player.gravity_engine = self.gravity_engine
            player.left_edge = self.platforms[0].left_edge + 10
            player.base_top_edge = self.platforms[0].top_edge - player.height
            player.set_top_edge(player.base_top_edge)

            self.player_health_bars.append(HealthBar(player, lambda: False))

        health_grid = Grid(Dimensions(0, 0, self.health_grid_length, self.health_grid_height), 2, 2)
        health_grid.turn_into_grid(self.player_health_bars, None, None)

        self.generator = Generator(self.players[0])
        self.hud.set_dimensions(health_grid.dimensions.right_edge, 0, self.hud_length, self.hud_height)

    def setup_enemies_and_platforms(self):
        """Creates the enemies and platforms of the game for starting out"""

        # One Long Platform
        self.platforms = [Platform(START_PLATFORM_LEFT_EDGE, START_PLATFORM_TOP_EDGE, START_PLATFORM_LENGTH, START_PLATFORM_HEIGHT)]
        self.enemies = []
        self.update_rightmost_platform()

    def run(self):
        """Runs all the code necessary in order for the platformer to work"""

        if self.intermediate_screen.has_finished():
            self.run_game_code()

        else:
            self.intermediate_screen.run()

    def run_game_code(self):
        """Runs all the code for running the game that runs when the intermediate screen is not being displayed"""

        self.run_player_and_enemies()
        self.run_all_collisions()

        # All the enemies and players should do something based on the updated collision they got from 'self.run_all_collisions()'
        for game_object in self.enemies + self.players:
            game_object.run_collisions()

        self.add_game_objects_to_history_keeper()
        self.run_side_scrolling()
        self.run_platform_generation()

    def run_player_and_enemies(self):
        """Runs all the code associated with the player's and enemies that is not collisions"""

        self.update_score()
        self.gravity_engine.run()
        self.powerups = list(filter(lambda item: item.right_edge >= 0, self.powerups))

        self.ammo_field.text = f"Ammo Left: {self.players[0].ammo_left}"

        for player in self.players:
            if player.platform_is_on is not None and not CollisionsEngine.is_collision(player, player.platform_is_on):
                player.set_is_on_platform(False, None)

            if player.hit_points_left <= 0 or not is_within_screen(player):
                self.run_player_respawn()

            if CollisionsEngine.is_collision(player, self.wall_of_death):
                self.reset_game()

            # So the player is moves before side scrolling happens
            player.run()

        for enemy in self.enemies:
            enemy.run_player_interactions(self.players)

            if enemy.hit_points_left <= 0:
                self.player_score += SCORE_FROM_KILLING_ENEMY

    def update_score(self):
        """Updates the HUD and the high score of the player"""

        if self.player_score > self.high_score:
            self.is_high_score = True
            self.high_score = self.player_score

        self.hud.update([self.player_score], self.high_score)

    def run_platform_generation(self):
        """Runs all the code for generating platforms"""

        if self.rightmost_platform.right_edge <= screen_length:
            difficulty = self.score_to_difficulty.get_y_coordinate(self.player_score)
            new_platform = self.generator.generate_platform(self.rightmost_platform, difficulty)
            self.platforms.append(new_platform)
            self.update_rightmost_platform()

            new_enemy = self.get_random_enemy(new_platform)
            self.enemies.append(new_enemy)
            self.gravity_engine.add_game_objects([new_enemy])

            self.number_of_platforms_generated += 1
            self.run_powerup_spawning(new_platform)

    def get_random_enemy(self, platform):
        """returns: Enemy; a random enemy"""

        enemy_types = [StraightEnemy, ChargingBull, BouncyEnemy]
        enemy_type = random.choice(enemy_types)

        return enemy_type(10, 20, platform)

    def run_powerup_spawning(self, new_platform):
        """Runs the spawning of powerups after a platform is generated: a powerup won't spawn everytime"""

        should_generate_powerup = is_random_chance(PROBABILITY_OF_GETTING_POWERUP_GENERATED)
        weapon_powerups = [BouncyProjectilePowerup, StraightProjectilePowerup]
        non_weapon_powerups = [HeartPowerup, AmmoPowerup]
        powerup_left_edge, powerup_top_edge = new_platform.horizontal_midpoint, new_platform.top_edge - Powerup.height

        if should_generate_powerup:
            should_generate_weapon = is_random_chance(PROBABILITY_OF_POWERUP_BEING_A_WEAPON)
            powerup_class_list = weapon_powerups if should_generate_weapon else non_weapon_powerups
            powerup_class = random.choice(powerup_class_list)
            self.powerups.append(powerup_class(powerup_left_edge, powerup_top_edge))

    def run_side_scrolling(self):
        """Makes the screen side scroll based off the player who is the farthest behind"""

        # First the players are sorted by the smallest left_edge and then the smallest player is taken
        farthest_back_player = list(sorted(self.players, key=lambda player: player.right_edge))[0]
        shortest_distance = farthest_back_player.right_edge

        # If the distance of the farthest back player is greater than the distance needed for sidescrolling then
        # All the objects in the game should be side scrolled
        if shortest_distance > SIDE_SCROLLING_START_DISTANCE:
            side_scrolling_distance = shortest_distance - SIDE_SCROLLING_START_DISTANCE
            self.side_scroll_all_objects(side_scrolling_distance)

    def side_scroll_objects(self, distance, game_objects):
        """Moves all the objects leftwards by the distance specified (side scrolling)"""

        for game_object in game_objects:
            game_object.update_for_side_scrolling(distance)

    def side_scroll_all_objects(self, side_scrolling_distance):
        """Side scrolls all the game objects by 'side_scrolling_distance'"""

        self.side_scroll_objects(side_scrolling_distance, self.players)
        self.side_scroll_objects(side_scrolling_distance, self.enemies)
        self.side_scroll_objects(side_scrolling_distance, self.platforms)
        self.side_scroll_objects(side_scrolling_distance, self.powerups)
        self.wall_of_death.update_for_side_scrolling(side_scrolling_distance)

    def get_code_ready_for_collisions(self):
        """Runs the necessary code to prepare for collisions: makes """

        player_components = []
        for player in self.players:
            player_components += player.get_collidable_components()
            player.reset_collision_data()

        updated_enemies = []
        enemy_components = []
        for enemy in self.enemies:
            enemy.reset_collision_data()

            if enemy.hit_points_left > 0 and enemy.platform.right_edge >= 0:
                updated_enemies.append(enemy)
                enemy_components += enemy.get_collidable_components()

        self.enemies = updated_enemies

        self.remove_platforms_not_within_screen()
        self.game_objects = player_components + enemy_components + self.platforms + self.powerups

    def remove_platforms_not_within_screen(self):
        """Removes all the platforms that are not within the screen"""

        updated_platforms = []
        for platform in self.platforms:
            if platform.right_edge >= 0:
                updated_platforms.append(platform)

            else:
                self.player_score += SCORE_FROM_PASSING_PLATFORM
        self.platforms = updated_platforms

    def run_player_respawn(self):
        """Makes the player respawn"""

        for player in self.players:
            player.run_respawning()

            if player.last_platform_was_on.horizontal_midpoint <= 0:
                difference = abs(player.last_platform_was_on.horizontal_midpoint)
                self.side_scroll_all_objects(-difference)

            player.left_edge = player.last_platform_was_on.horizontal_midpoint
            player.top_edge = player.last_platform_was_on.top_edge - player.height
            self.remove_enemies_on_platform(player.last_platform_was_on)

        self.wall_of_death.total_time += WALL_OF_DEATH_TIME_INCREASE_AFTER_PLAYER_DEATH
        self.powerups = []
        HistoryKeeper.last_objects = {}
        self.gravity_engine.reset()
        self.intermediate_screen.display("Player Respawn", RESPAWN_MESSAGE_TIME)

    def remove_enemies_on_platform(self, platform):
        """Removes all the enemies that are on that platform"""

        enemies_not_on_platform = []

        for enemy in self.enemies:
            if enemy.platform != platform:
                enemies_not_on_platform.append(enemy)

        self.enemies = enemies_not_on_platform

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
        self.number_of_platforms_generated = 0
        self.powerups = []
        self.wall_of_death.reset()

        high_score_message = f"New High Score: {self.high_score}"
        non_high_score_message = f"Score: {self.player_score}"
        message = high_score_message if self.is_high_score else non_high_score_message
        self.intermediate_screen.display(message, DEATH_MESSAGE_TIME)

    def run_all_collisions(self):
        """Runs all the collisions between the player, projectiles, and enemies"""

        self.get_code_ready_for_collisions()

        for i in range(len(self.game_objects)):
            object1 = self.game_objects[i]

            for j in range(i, len(self.game_objects)):
                object2 = self.game_objects[j]

                collision_is_possible = len(object1.object_type) != len(object2.object_type)
                collision_has_happened = collision_is_possible and CollisionsEngine.is_collision(object1, object2)

                # The 'self.run_object_collisions' should only be called if the main object is not a platform
                if collision_has_happened and not self.is_platform(object1):
                    self.run_object_collisions(object1, object2)

                if collision_has_happened and not self.is_platform(object2):
                    self.run_object_collisions(object2, object1)

    def run_object_collisions(self, main_object, other_object):
        """Runs the collisions between the 'main_object' and the 'other_object;' the main_object acts upon the other_object.
        By act upon I mean damages the other_object, moves the other_object, etc."""

        if self.is_player(main_object) or self.is_player_weapon(main_object):
            self.run_player_collisions(main_object, other_object)

        elif self.is_enemy(main_object) or self.is_enemy_weapon(main_object):
            self.run_enemy_collisions(main_object, other_object)

        elif self.is_powerup(main_object) and self.is_player(other_object):
            main_object.run_player_collision(other_object)

            # Removes it from the screen so it is deleted: can't delete here because that would cause issues with modifying
            # a list while it is being iterated over
            main_object.left_edge = -1000

    def run_player_collisions(self, main_object, other_object):
        """Runs the collisions for when the player is the main object"""

        collision_function_parameters = [other_object, main_object.index]
        has_collided_with_enemy = self.is_enemy_weapon(other_object) or self.is_enemy(other_object)

        if self.is_player(main_object) and self.is_platform(other_object):
            main_object.run_inanimate_object_collision(*collision_function_parameters)

        elif self.is_player_weapon(main_object) and self.is_platform(other_object):
            main_object.user.run_inanimate_object_collision(*collision_function_parameters)

        elif self.is_player_weapon(main_object) and has_collided_with_enemy:
            main_object.user.run_enemy_collision(*collision_function_parameters)

    def run_enemy_collisions(self, main_object, other_object):
        """Runs the collisions for when the enemy is the main object"""

        collision_function_parameters = [other_object, main_object.index]
        if self.is_enemy(main_object) and self.is_platform(other_object):
            main_object.run_inanimate_object_collision(*collision_function_parameters)

        elif self.is_enemy_weapon(main_object) and self.is_platform(other_object):
            main_object.user.run_inanimate_object_collision(*collision_function_parameters)

        elif self.is_enemy(main_object) and self.is_player(other_object):
            main_object.run_enemy_collision(*collision_function_parameters)

        elif self.is_enemy_weapon(main_object) and self.is_player(other_object):
            main_object.user.run_enemy_collision(*collision_function_parameters)

    def add_game_objects_to_history_keeper(self):
        """Adds all the game objects to the HistoryKeeper"""

        for game_object in self.enemies + self.players:
            self.add_collidable_components(game_object.get_collidable_components())

        self.add_collidable_components(self.platforms)

    def add_collidable_components(self, component_list):
        """Adds all the components in the component_list to the History Keeper"""

        for component in component_list:
            if component.is_addable:
                component.name = id(component)
                HistoryKeeper.add(component, component.name, needs_dimensions_only=True)

    def run_on_close(self):
        """Runs what should happen when the game is closed (save the high scores)"""

        file = open("games/platformer/high_scores.txt", "w+")
        file.write(f"high_scores:[{self.high_score}]")
        file.close()

    def get_components(self):
        """returns: Component[]; all the components that should be rendered"""

        game_components = []
        for game_object in self.players + self.enemies:
            game_components += game_object.get_components()

        game_components += self.player_health_bars + self.platforms + self.powerups + [self.wall_of_death] + [self.hud]
        return game_components if self.intermediate_screen.has_finished() else self.intermediate_screen.get_components()

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

    def is_powerup(self, game_object):
        """returns: boolean; if the game_object is a platform --> object type would be 'Platform'"""

        return len(game_object.object_type) == 9








