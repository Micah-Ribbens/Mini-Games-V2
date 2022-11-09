from base.fraction import Fraction
from base.important_variables import *
from base.lines import Point
from base.paths import SimplePath
from base.velocity_calculator import VelocityCalculator

## Player
### Dimensions
PLAYER_HEIGHT = VelocityCalculator.get_measurement(screen_height, 15)
PLAYER_LENGTH = VelocityCalculator.get_measurement(screen_length, 5)

### Movement
PLAYER_JUMP_DISPLACEMENT = screen_height * .3
PLAYER_TIME_TO_JUMP_VERTEX = .55
PLAYER_RUNNING_DECELERATION_TIME = .3
PLAYER_INVINCIBILITY_TOTAL_TIME = 1
PLAYER_TIME_TO_GET_MAX_VELOCITY = .2
PLAYER_MAX_HORIZONTAL_VELOCITY = VelocityCalculator.get_velocity(screen_length, 450)

### Other
PLAYER_OBJECT_TYPE = "Player"
PLAYER_TOTAL_HIT_POINTS = 60
PLAYER_BASE_LEFT_EDGE = 100
PLAYER_BASE_TOP_EDGE = 0

## Generator
SIDE_SCROLLING_START_DISTANCE = VelocityCalculator.get_measurement(screen_length, 33)
# The minimum amount of the next platform that has to be visible when the player gets to the end of the previous platform
MINIMUM_PLATFORM_LENGTH_VISIBLE = VelocityCalculator.get_measurement(screen_length, 20)

## Scoring
SCORE_FROM_PASSING_PLATFORM = 100
SCORE_FROM_KILLING_ENEMY = 250

## Weapons
BASE_WEAPON_AMMO = 10

## Powerups
AMMO_INCREASE_FROM_POWERUP = 5
HEALTH_INCREASE_FROM_HEART = 5
PROBABILITY_OF_GETTING_POWERUP_GENERATED = Fraction(2, 7)
# If the player has a weapon and they pick up the powerup of the same weapon that weapon should be upgraded
DAMAGE_INCREASE_FROM_DUPLICATE_WEAPON_PICKUP = 5
# Probabilities of a powerup being a specific type
PROBABILITY_OF_POWERUP_BEING_A_WEAPON = Fraction(30, 100)
PROBABILITY_OF_POWERUP_NOT_BEING_A_WEAPON = PROBABILITY_OF_POWERUP_BEING_A_WEAPON.get_fraction_to_become_one()

## Wall of Death
TIME_BEFORE_WALL_OF_DEATH_STARTS_MOVING = 2
WALL_OF_DEATH_TIME_INCREASE_AFTER_PLAYER_DEATH = 1
TIME_GAME_HAS_RUN_TO_WALL_OF_DEATH_VELOCITY = SimplePath(Point(0, PLAYER_MAX_HORIZONTAL_VELOCITY * .3),
                                                         [Point(5, PLAYER_MAX_HORIZONTAL_VELOCITY * .5),
                                                          Point(30, PLAYER_MAX_HORIZONTAL_VELOCITY * .6),
                                                          Point(60, PLAYER_MAX_HORIZONTAL_VELOCITY * .7),
                                                          Point(120, PLAYER_MAX_HORIZONTAL_VELOCITY * .75),
                                                          Point(float("inf"), PLAYER_MAX_HORIZONTAL_VELOCITY * .75)])




