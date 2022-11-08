from base.fraction import Fraction
from base.important_variables import *
from base.velocity_calculator import VelocityCalculator

jump_displacement = screen_height * .3
time_to_vertex_of_jump = .55
player_height = VelocityCalculator.get_measurement(screen_height, 15)
side_scrolling_start_distance = VelocityCalculator.get_measurement(screen_length, 33)
# The minimum amount of the next platform that has to be visible when the player gets to the end of the previous platform
min_platform_length_visible = VelocityCalculator.get_measurement(screen_length, 20)

# Scoring
score_from_passing_platform = 100
score_from_killing_enemy = 250

# Weapons
base_weapon_ammo = 10

# Powerups
ammo_increase_from_powerup = 5
health_increase_from_heart = 5
probability_of_getting_powerup_generated = Fraction(2, 7)
# If the player has a weapon and they pick up the powerup of the same weapon that weapon should be upgraded
damage_increase_from_duplicate_weapon_pickup = 5
# Probabilities of a powerup being a specific type
weapon_powerup_probability = Fraction(30, 100)
non_weapon_powerup_probability = weapon_powerup_probability.get_fraction_to_become_one()


