import random

from base.engines import CollisionsEngine
from base.file_reader import FileReader
from base.utility_functions import key_is_hit
from base.velocity_calculator import VelocityCalculator
from base.important_variables import *
from games.no_internet_game.character import Player
from gui_components.component import Component
from gui_components.hud import HUD
from gui_components.screen import Screen
from pygame_library.keys import KEY_W

class NoInternetGameScreen(Screen):
    enemies = []
    spawnable_enemies = [] # Enemies that can cause spawning
    ground_top_edge = .9 * screen_height

    tree_length = VelocityCalculator.get_measurement(screen_length, 8)

    fish_length = VelocityCalculator.get_measurement(screen_length, 10)
    fish_height = VelocityCalculator.get_measurement(screen_height, 13)
    low_fish_top_edge = ground_top_edge - fish_height

    base_object_velocities = Player.forwards_velocity
    object_velocities = base_object_velocities
    max_velocity = base_object_velocities * 2.5
    velocity_increase = object_velocities * .1

    player_points = 0
    high_score = 0
    hud = HUD(1, [], screen_length, screen_height * .08, 1, None)
    player = Player([KEY_A, KEY_D, KEY_W], ground_top_edge)
    game_is_paused = False

    def __init__(self):
        super().__init__("games/no_internet_game/images/background.png")
        self.spawn_random_enemy()

        file_reader = FileReader("games/no_internet_game/high_scores.txt")
        self.high_score = file_reader.get_int("high_score")

    def request_enemy_spawn(self):
        is_double_tree = len(self.enemies) >= 2 and self.enemies[1].height == self.second_tree_height

        can_spawn_enemy = len(self.spawnable_enemies) != 0 and self.spawnable_enemies.__contains__(self.enemies[0])

        if can_spawn_enemy:
            index_cutoff = 2 if is_double_tree else 1
            print(is_double_tree)
            self.spawnable_enemies = self.spawnable_enemies[index_cutoff:]
            self.spawn_random_enemy()

    def request_points(self, enemy):
        is_tree = enemy.path_to_image == "games/no_internet_game/images/tree.png"

        if not is_tree or enemy.height == self.tree_height:
            self.player_points += 100

        velocity_points_threshold = 1000

        if self.player_points % velocity_points_threshold == 0:
            self.object_velocities += self.velocity_increase

        self.object_velocities = min(self.object_velocities, self.max_velocity)

    def spawn_random_enemy(self):
        spawn_functions = [self.spawn_fish, self.spawn_tree]
        random.choice(spawn_functions)()

    def add_enemy(self, enemy):
        self.enemies.append(enemy)
        self.spawnable_enemies.append(enemy)

    def spawn_fish(self):
        top_edge = random.choice([self.low_fish_top_edge, self.medium_fish_top_edge, self.high_fish_top_edge])

        fish = Component("games/no_internet_game/images/enemy.png")
        fish.number_set_dimensions(screen_length, top_edge, self.fish_length, self.fish_height)
        self.add_enemy(fish)

    def spawn_tree(self):
        number_of_trees = random.choice([1, 2])

        tree = Component("games/no_internet_game/images/tree.png")
        tree.number_set_dimensions(screen_length, self.ground_top_edge - self.tree_height, self.tree_length, self.tree_height)
        self.add_enemy(tree)

        if number_of_trees == 2:
            tree2 = Component("games/no_internet_game/images/tree.png")
            tree_height = self.second_tree_height
            tree2.number_set_dimensions(tree.right_edge, self.ground_top_edge - tree_height, self.tree_length * .7, tree_height)
            self.add_enemy(tree2)

    def run(self):
        if key_is_hit(KEY_S) and self.game_is_paused:
            self.reset_game()
            self.game_is_paused = False
            self.player.game_is_paused = False

        elif self.game_is_paused:
            # print("GAME PAUSED")
            return

        spawn_starter_location = 100
        self.high_score = max(self.player_points, self.high_score)
        self.hud.update([self.player_points], self.high_score)

        # print(len(self.enemies))

        if len(self.enemies) > 0 and self.enemies[0].right_edge <= spawn_starter_location:
            # print("REQUEST SPAWN")
            self.request_enemy_spawn()

        if len(self.enemies) == 0:
            # print("SPAWN RANDOM ENEMY")
            self.spawn_random_enemy()

        alive_enemies = []
        for enemy in self.enemies:
            enemy.left_edge -= VelocityCalculator.calculate_distance(self.object_velocities)

            if enemy.right_edge >= 0:
                alive_enemies.append(enemy)

            else:
                self.request_points(enemy)

            if CollisionsEngine.is_collision(self.player, enemy):
                self.game_is_paused = True
                self.player.game_is_paused = True

        self.enemies = alive_enemies

    def get_components(self):
        return [self.hud, self.player] + self.enemies

    def reset_game(self):
        self.player.reset()
        self.enemies, self.spawnable_enemies = [], []
        self.player_points = 0
        self.object_velocities = self.base_object_velocities

    def run_on_close(self):
        """Saves the high score"""

        file_writer = open("games/no_internet_game/high_scores.txt", "w+")
        file_writer.write(f"high_score:{self.high_score}")

    @property
    def high_fish_top_edge(self):
        buffer = screen_height * .1
        return self.player.initial_distance - buffer - self.fish_height

    @property
    def tree_height(self):
        return self.player.vertex_height * .5

    @property
    def medium_fish_top_edge(self):
        return self.ground_top_edge - self.player.vertex_height * .6

    @property
    def second_tree_height(self):
        return self.tree_height * .7
