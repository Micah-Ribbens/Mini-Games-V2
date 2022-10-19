from base.engines import CollisionsEngine
from base.velocity_calculator import VelocityCalculator
from games.bird_shooter.bullet import Bullet
from games.bird_shooter.enemy import Enemy
from gui_components.hud import HUD
from gui_components.intermediate_screen import IntermediateScreen
from gui_components.screen import Screen
from base.important_variables import *
from games.bird_shooter.player import Player


class BirdShooterScreen(Screen):
    # Player Position and Keys
    middle_of_screen = screen_length / 2
    total_buffer = (Player.turret_length - Player.cap_extension) * 2 + VelocityCalculator.get_measurement(screen_length, 2)

    individual_buffer = total_buffer / 2

    players_keys = [[KEY_A, KEY_D, KEY_W, KEY_S, KEY_F, KEY_G],
                    [KEY_LEFT, KEY_RIGHT, KEY_UP, KEY_DOWN, KEY_QUESTION_MARK, KEY_PERIOD]]

    player_boundaries = [[0, middle_of_screen - Player.length - individual_buffer, 0, screen_height - Player.height],
                         [middle_of_screen + individual_buffer, screen_length - Player.length, 0, screen_height - Player.height]]
    # Other Player Stuff
    player1 = Player(players_keys[0], 1, player_boundaries[0], True)
    player2 = Player(players_keys[1], 2, player_boundaries[1], False)
    player1_score = 0
    player2_score = 0
    # Miscellaneous Stuff
    bullets = []
    enemy = Enemy()
    high_score = 0
    hud = HUD(2, [], screen_length, screen_height * .1, 1, None)
    intermediate_screen = IntermediateScreen()

    def __init__(self):
        super().__init__("games/bird_shooter/images/background.png")
        self.center_players()

    def run(self):

        self.intermediate_screen.run()

        if self.intermediate_screen.has_finished():
            self.intermediate_screen.run()
            self.run_collisions()
            normal_high_score_text = "Player1" if self.player1_score > self.player2_score else "Player2"
            high_score_text = "Tie" if self.player1_score == self.player2_score else normal_high_score_text
            self.hud.update([self.player1_score, self.player2_score], high_score_text)

    def run_collisions(self):
        self.run_bullet_collisions()
        enemy_has_hit_player1 = CollisionsEngine.is_collision(self.enemy, self.player1)
        enemy_has_hit_player2 = CollisionsEngine.is_collision(self.enemy, self.player2)

        if enemy_has_hit_player1 or self.enemy.right_edge < 0:
            self.run_player_scoring(False)

        if enemy_has_hit_player2 or self.enemy.left_edge > screen_length:
            self.run_player_scoring(True)

    def run_bullet_collisions(self):
        self.bullets += self.player1.new_bullets + self.player2.new_bullets

        for i in range(len(self.bullets)):
            base_stun_time = .4
            stun_time = base_stun_time * self.bullets[i].total_hits_to_destroy
            bullet1: Bullet = self.bullets[i]

            bullet_has_hit_player1 = CollisionsEngine.is_collision(self.player1, bullet1)
            bullet_has_hit_player2 = CollisionsEngine.is_collision(self.player2, bullet1)
            bullet_has_hit_enemy = CollisionsEngine.is_collision(bullet1, self.enemy)

            if bullet_has_hit_player1:
                self.player1.stun(stun_time)

            elif bullet_has_hit_player2:
                self.player2.stun(stun_time)

            if bullet_has_hit_enemy and self.enemy.is_moving_right != bullet1.is_moving_right:
                self.enemy.hits_left_to_change_direction -= bullet1.total_hits_to_destroy

            if bullet_has_hit_player1 or bullet_has_hit_player2 or bullet_has_hit_enemy:
                bullet1.hits_left_to_destroy = 0
                continue

            for j in range(i, len(self.bullets) - i):
                bullet2: Bullet = self.bullets[j]

                if bullet1 != bullet2 and CollisionsEngine.is_collision(bullet1, bullet2):
                    bullet1.hits_left_to_destroy -= bullet2.total_hits_to_destroy
                    bullet2.hits_left_to_destroy -= bullet2.total_hits_to_destroy

        self.bullets = list(filter(lambda item: item.hits_left_to_destroy > 0, self.bullets))

    def get_components(self):
        game_components = [self.hud, self.enemy, self.player1, self.player2] + self.bullets
        return game_components if self.intermediate_screen.has_finished() else self.intermediate_screen.get_components()

    def run_player_scoring(self, player1_has_scored):
        self.player1.reset()
        self.player2.reset()
        self.enemy.reset()

        self.player1_score += 1 if player1_has_scored else 0
        self.player2_score += 1 if not player1_has_scored else 0

        message = "Player1 Has Scored" if player1_has_scored else "Player2 Has Scored"
        self.intermediate_screen.display(message, .75)
        self.center_players()

    def center_players(self):
        self.player1.left_edge = 0
        self.player2.left_edge = screen_length - self.player2.length

